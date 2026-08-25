"""
Gerador de DDL (CREATE TABLE) a partir do modelo de campos de um copybook.

Mapeamento COBOL -> DB2 (deterministico, baseado no PIC/USAGE reais do copybook):

  PIC X(n) / A(n)              -> CHAR(n)          (VARCHAR(n) se n > 255)
  PIC 9(n)  DISPLAY            -> DECIMAL(n)       (INTEGER se n<=9 e sem decimais opcional)
  PIC 9(i)V9(d)               -> DECIMAL(i+d, d)
  PIC S9(n) COMP-3            -> DECIMAL(n)        (packed decimal)
  PIC 9(n) COMP / COMP-4      -> SMALLINT/INTEGER/BIGINT conforme n
  campo/grupo -NUL            -> coluna permite NULL (senao NOT NULL)

O nome da coluna e o nome do campo COBOL com '-' trocado por '_' (padrao SQL).
Campos FILLER sao ignorados. Grupos viram prefixo/observacao, nao coluna.
"""
from __future__ import annotations

from .copybook_parser import Field, PicInfo, iter_elementary


def _col_name(cobol_name: str) -> str:
    col = cobol_name.replace('-', '_').upper()
    # SQL nao permite identificador iniciado por digito (ex: 1ST_...)
    if col and col[0].isdigit():
        col = 'C_' + col
    return col


def sql_type(pic: PicInfo) -> str:
    """Traduz PicInfo em tipo SQL DB2."""
    if pic.category == 'alfanumerico':
        n = max(pic.length, 1)
        return f'CHAR({n})' if n <= 255 else f'VARCHAR({n})'

    if pic.category == 'numerico':
        i, d = pic.integer_digits, pic.decimal_digits
        total = i + d
        if d > 0:
            return f'DECIMAL({total},{d})'
        # inteiro puro
        if pic.usage in ('COMP', 'COMP-4', 'BINARY'):
            if total <= 4:
                return 'SMALLINT'
            if total <= 9:
                return 'INTEGER'
            return 'BIGINT'
        # DISPLAY ou COMP-3: preserva precisao com DECIMAL
        return f'DECIMAL({max(total,1)})'

    # desconhecido -> texto seguro
    return f'CHAR({max(pic.length, 1)})'


def gerar_ddl(table_name: str, campos: list, schema: str = None,
              extra_cols: list = None) -> str:
    """Gera o CREATE TABLE de uma tabela a partir dos campos do copybook.

    table_name : nome da tabela (ex: PRODRDSDS)
    campos     : arvore de Field (saida de parse_copybook)
    schema     : schema opcional (ex: PRODESP)
    extra_cols : lista de linhas de coluna adicionais (ex: ROWID) ja formatadas
    """
    # cada item: (definicao_sem_virgula, comentario)
    itens = []
    vistos = set()
    for trilha, campo in iter_elementary(campos):
        col = _col_name(campo.name)
        if col in vistos:
            # nomes repetidos (ex: 1ST-*) - desambigua com sufixo
            i = 2
            while f'{col}_{i}' in vistos:
                i += 1
            col = f'{col}_{i}'
        vistos.add(col)
        tipo = sql_type(campo.pic)
        null = 'NULL' if campo.nullable else 'NOT NULL'
        comentario = f'-- {campo.pic.raw}' + (f' {campo.pic.usage}' if campo.pic.usage != 'DISPLAY' else '')
        definicao = f'{col:<24} {tipo:<16} {null}'
        itens.append((definicao, comentario))

    if extra_cols:
        for ec in extra_cols:
            itens.append((ec.rstrip(','), ''))

    # monta o corpo com virgula em todos menos o ultimo
    linhas = []
    for idx, (definicao, comentario) in enumerate(itens):
        virgula = ',' if idx < len(itens) - 1 else ''
        sufixo = f'  {comentario}' if comentario else ''
        linhas.append(f'    {definicao}{virgula}{sufixo}')

    full_name = f'{schema}.{table_name}' if schema else table_name
    body = '\n'.join(linhas)
    return f'CREATE TABLE {full_name} (\n{body}\n);'


def gerar_ddl_de_arquivo(path, table_name: str = None, schema: str = None) -> str:
    from pathlib import Path
    from .copybook_parser import parse_file
    campos = parse_file(path)
    if table_name is None:
        table_name = Path(path).stem.replace('MAPA_', '').upper()
    return gerar_ddl(table_name, campos, schema=schema)
