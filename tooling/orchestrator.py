"""
Orquestrador: gera DDL + massa de dados de TODAS as tabelas a partir dos
programas COBOL convertidos e dos copybooks.

Fluxo:
  1. Varre os programas e extrai tabelas/colunas/host-vars (sql_extractor)
  2. Le os copybooks disponiveis e indexa campo -> PicInfo (copybook_parser)
  3. Casa cada COLUNA SQL com o CAMPO do copybook via host-variable
     (a host-var :GER-CHASSI-X corresponde ao campo GER-CHASSI-X no copybook)
  4. Gera DDL usando o tipo REAL do copybook; se o campo nao estiver disponivel
     (copybook faltante), usa fallback por heuristica e marca como INFERIDO
  5. Gera massa de dados

Enquanto os 217 copybooks reais nao chegam, a maioria dos campos usa fallback.
Quando chegarem, basta apontar --copybooks para a pasta e a fidelidade sobe.
"""
from __future__ import annotations

import re
from pathlib import Path

from .copybook_parser import parse_file, iter_elementary, PicInfo
from .sql_extractor import extrair_de_arquivo, TableInfo
from .ddl_generator import _col_name, sql_type
from .data_generator import _valor_campo, _sql_literal, _dominio
import random


def _eh_programa(txt: str) -> bool:
    u = txt.upper()
    return 'PROGRAM-ID' in u or 'IDENTIFICATION DIVISION' in u


def indexar_copybooks(pastas: list) -> dict:
    """Indexa todos os campos elementares dos copybooks: {NOME_CAMPO: PicInfo}.
    NOME_CAMPO em maiusculo com hifens (como aparece no copybook)."""
    idx = {}
    for pasta in pastas:
        pasta = Path(pasta)
        if not pasta.exists():
            continue
        for f in pasta.iterdir():
            if not f.is_file():
                continue
            txt = f.read_text(encoding='latin-1', errors='ignore')
            if _eh_programa(txt):
                continue  # so copybooks
            try:
                campos = parse_file(f)
            except Exception:
                continue
            for _tr, c in iter_elementary(campos):
                idx.setdefault(c.name.upper(), c.pic)
    return idx


def coletar_tabelas(pasta_programas) -> dict:
    """Une as tabelas de todos os programas em um dicionario global."""
    pasta = Path(pasta_programas)
    global_tabs = {}
    for f in pasta.iterdir():
        if not f.is_file():
            continue
        txt = f.read_text(encoding='latin-1', errors='ignore')
        if not _eh_programa(txt):
            continue
        tabs = extrair_de_arquivo(f)
        for key, ti in tabs.items():
            if key not in global_tabs:
                global_tabs[key] = ti
            else:
                g = global_tabs[key]
                for c in ti.columns:
                    if c not in g.columns:
                        g.columns.append(c)
                g.keys |= ti.keys
                g.col_to_hostvar.update(ti.col_to_hostvar)
                g.programs |= ti.programs
    return global_tabs


def _pic_fallback(coluna: str, hostvar: str) -> PicInfo:
    """Quando o copybook do campo nao esta disponivel, infere um PIC pela
    heuristica do nome (marcado como inferido)."""
    dom = _dominio(hostvar or coluna)
    if dom in ('cpf', 'cnpj', 'renavam'):
        return PicInfo(raw='9(011)[INFERIDO]', category='numerico', length=11, integer_digits=11)
    if dom == 'data':
        return PicInfo(raw='9(008)[INFERIDO]', category='numerico', length=8, integer_digits=8)
    if dom == 'hora':
        return PicInfo(raw='9(006)[INFERIDO]', category='numerico', length=6, integer_digits=6)
    if dom == 'municipio':
        return PicInfo(raw='9(005)[INFERIDO]', category='numerico', length=5, integer_digits=5)
    if dom == 'ano':
        return PicInfo(raw='9(004)[INFERIDO]', category='numerico', length=4, integer_digits=4)
    if dom == 'uf':
        return PicInfo(raw='X(002)[INFERIDO]', category='alfanumerico', length=2)
    if dom in ('placa',):
        return PicInfo(raw='X(007)[INFERIDO]', category='alfanumerico', length=7)
    if dom in ('chassi', 'nome'):
        return PicInfo(raw='X(030)[INFERIDO]', category='alfanumerico', length=30)
    if hostvar and hostvar.upper().endswith('-X'):
        return PicInfo(raw='X(020)[INFERIDO]', category='alfanumerico', length=20)
    return PicInfo(raw='X(030)[INFERIDO]', category='alfanumerico', length=30)


def resolver_colunas(ti: TableInfo, copy_idx: dict):
    """Para cada coluna da tabela, resolve (coluna_sql, PicInfo, origem, nullable).
    origem: 'copybook' (fiel) ou 'inferido' (fallback)."""
    resolvidas = []
    for col in ti.columns:
        hv = ti.col_to_hostvar.get(col, '')
        pic = None
        origem = 'inferido'
        # tenta casar host-var com o campo do copybook
        candidatos = []
        if hv:
            candidatos.append(hv.upper())
            # host-var costuma ter sufixo -X; o campo do copybook pode nao ter
            if hv.upper().endswith('-X'):
                candidatos.append(hv.upper()[:-2])
        candidatos.append(col.upper().replace('_', '-'))
        for cand in candidatos:
            if cand in copy_idx:
                pic = copy_idx[cand]
                origem = 'copybook'
                break
        if pic is None:
            pic = _pic_fallback(col, hv)
        nullable = col in ti.keys and False or True  # colunas nao-chave: nullable
        nullable = col not in ti.keys
        if col.upper().startswith('ROWID'):
            nullable = False
        resolvidas.append((col, pic, origem, nullable, hv))
    return resolvidas


def gerar_ddl_tabela(ti: TableInfo, copy_idx: dict) -> str:
    resolvidas = resolver_colunas(ti, copy_idx)
    itens = []
    for col, pic, origem, nullable, hv in resolvidas:
        colname = _col_name(col)
        tipo = sql_type(pic)
        null = 'NULL' if nullable else 'NOT NULL'
        tag = '' if origem == 'copybook' else '  [INFERIDO]'
        itens.append((f'{colname:<28} {tipo:<16} {null}', f'-- {pic.raw}{tag}'))
    # chaves
    pk = [(_col_name(c)) for c in ti.columns if c in ti.keys]
    linhas = []
    for idx, (d, cmt) in enumerate(itens):
        virgula = ',' if (idx < len(itens) - 1 or pk) else ''
        linhas.append(f'    {d}{virgula}  {cmt}')
    if pk:
        linhas.append(f'    PRIMARY KEY ({", ".join(pk)})')
    return f'CREATE TABLE {ti.full_name} (\n' + '\n'.join(linhas) + '\n);'


def gerar_massa_tabela(ti: TableInfo, copy_idx: dict, n: int = 10, seed: int = 42) -> str:
    resolvidas = resolver_colunas(ti, copy_idx)
    if not resolvidas:
        return f'-- (sem colunas para {ti.full_name})'
    rng = random.Random(seed)
    cols = [_col_name(c) for c, *_ in resolvidas]
    col_list = ', '.join(cols)
    out = []
    for r in range(n):
        borda = 'min' if r == 0 else ('max' if r == 1 else None)
        vals = []
        for (col, pic, origem, nullable, hv) in resolvidas:
            # campo fake so com pic para reusar _valor_campo
            from .copybook_parser import Field
            campo = Field(level=5, name=(hv or col).upper(), pic=pic, nullable=nullable)
            if nullable and (r == 2 or rng.random() < 0.15):
                vals.append('NULL')
            else:
                vals.append(_sql_literal(_valor_campo(campo, rng, borda)))
        out.append(f'INSERT INTO {ti.full_name} ({col_list}) VALUES ({", ".join(vals)});')
    return '\n'.join(out)


def gerar_tudo(pasta_programas, pastas_copybooks: list, out_dir, n_massa: int = 10):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    copy_idx = indexar_copybooks(pastas_copybooks)
    tabelas = coletar_tabelas(pasta_programas)

    ddl_all = ['-- DDL gerada automaticamente a partir dos programas + copybooks',
               f'-- Tabelas: {len(tabelas)} | Campos indexados de copybooks: {len(copy_idx)}',
               '']
    massa_all = ['-- Massa de dados sintetica gerada automaticamente', '']
    resumo = []
    for key in sorted(tabelas):
        ti = tabelas[key]
        ddl_all.append(gerar_ddl_tabela(ti, copy_idx))
        ddl_all.append('')
        massa_all.append(gerar_massa_tabela(ti, copy_idx, n=n_massa))
        massa_all.append('')
        resolvidas = resolver_colunas(ti, copy_idx)
        fieis = sum(1 for *_r, o, _n, _h in [(r[0], r[1], r[2], r[3], r[4]) for r in resolvidas] if o == 'copybook')
        fieis = sum(1 for r in resolvidas if r[2] == 'copybook')
        resumo.append((ti.full_name, len(ti.columns), fieis, len(ti.columns) - fieis, len(ti.programs)))

    (out / 'schema.sql').write_text('\n'.join(ddl_all), encoding='utf-8')
    (out / 'massa.sql').write_text('\n'.join(massa_all), encoding='utf-8')

    # relatorio de cobertura
    rel = ['# Relatorio de geracao', '',
           f'- Tabelas: {len(tabelas)}',
           f'- Campos de copybook indexados: {len(copy_idx)}', '',
           '| Tabela | Colunas | Fieis (copybook) | Inferidas | Programas |',
           '|--------|--------:|-----------------:|----------:|----------:|']
    for nome, ncol, fiel, inf, nprog in resumo:
        rel.append(f'| {nome} | {ncol} | {fiel} | {inf} | {nprog} |')
    (out / 'relatorio.md').write_text('\n'.join(rel), encoding='utf-8')

    return {
        'tabelas': len(tabelas),
        'campos_copybook': len(copy_idx),
        'out': str(out),
    }


def gerar_para_web(pasta_programas, pastas_copybooks: list, n_massa: int = 10) -> dict:
    """Versao em memoria para a interface web. Nao escreve arquivos.

    Retorna:
      {
        'resumo': {'tabelas': N, 'campos_copybook': N, 'colunas_fieis': N,
                   'colunas_inferidas': N, 'fidelidade': 99.7},
        'schema': '<DDL completa>',
        'massa': '<INSERTs>',
        'tabelas': [ {nome, colunas, fieis, inferidas, programas}, ... ]
      }
    """
    copy_idx = indexar_copybooks(pastas_copybooks)
    tabelas = coletar_tabelas(pasta_programas)

    ddl_all = []
    massa_all = []
    tab_rows = []
    total_fieis = 0
    total_inf = 0
    for key in sorted(tabelas):
        ti = tabelas[key]
        ddl_all.append(gerar_ddl_tabela(ti, copy_idx))
        massa_all.append(gerar_massa_tabela(ti, copy_idx, n=n_massa))
        resolvidas = resolver_colunas(ti, copy_idx)
        fieis = sum(1 for r in resolvidas if r[2] == 'copybook')
        inf = len(resolvidas) - fieis
        total_fieis += fieis
        total_inf += inf
        tab_rows.append({
            'nome': ti.full_name,
            'colunas': len(ti.columns),
            'fieis': fieis,
            'inferidas': inf,
            'programas': len(ti.programs),
        })

    total_col = total_fieis + total_inf
    fidelidade = round(100 * total_fieis / total_col, 1) if total_col else 0.0
    return {
        'resumo': {
            'tabelas': len(tabelas),
            'campos_copybook': len(copy_idx),
            'colunas_fieis': total_fieis,
            'colunas_inferidas': total_inf,
            'fidelidade': fidelidade,
        },
        'schema': '\n\n'.join(ddl_all),
        'massa': '\n\n'.join(massa_all),
        'tabelas': tab_rows,
    }


# ---------------------------------------------------------------------------
# Materializacao do banco de dados local (SQLite)
# ---------------------------------------------------------------------------
def _db2_para_sqlite(sql: str) -> str:
    """Converte a DDL/DML DB2 para dialeto SQLite (para o banco local)."""
    s = re.sub(r'\bDECIMAL\(\d+(,\d+)?\)', 'NUMERIC', sql)
    s = re.sub(r'\b(CHAR|VARCHAR)\(\d+\)', 'TEXT', s)
    s = s.replace('SMALLINT', 'INTEGER').replace('BIGINT', 'INTEGER')
    # SQLite nao usa schema.tabela -> troca ponto por underscore no nome da tabela
    s = re.sub(r'CREATE TABLE\s+([A-Z0-9_]+)\.([A-Z0-9_]+)', r'CREATE TABLE \1_\2', s)
    s = re.sub(r'INSERT INTO\s+([A-Z0-9_]+)\.([A-Z0-9_]+)', r'INSERT INTO \1_\2', s)
    return s


def gerar_banco_local(pasta_programas, pastas_copybooks: list, db_path,
                      n_massa: int = 10) -> dict:
    """Gera a estrutura, cria um banco SQLite fisico e popula com a massa.

    Retorna estatisticas: tabelas criadas, linhas inseridas, erros e caminho do .db.
    """
    import sqlite3

    dados = gerar_para_web(pasta_programas, pastas_copybooks, n_massa=n_massa)

    db_path = Path(db_path)
    if db_path.exists():
        db_path.unlink()  # recria do zero
    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()

    # 1. cria as tabelas
    tabelas_ok = 0
    erros_ddl = []
    for stmt in dados['schema'].split(';'):
        s = stmt.strip()
        if not s.upper().startswith('CREATE TABLE'):
            continue
        try:
            cur.execute(_db2_para_sqlite(s) + ';')
            tabelas_ok += 1
        except Exception as e:
            erros_ddl.append(str(e))

    # 2. popula com a massa
    linhas_ok = 0
    erros_ins = []
    for stmt in dados['massa'].splitlines():
        s = stmt.strip()
        if not s.upper().startswith('INSERT'):
            continue
        try:
            cur.execute(_db2_para_sqlite(s))
            linhas_ok += 1
        except Exception as e:
            if len(erros_ins) < 10:
                erros_ins.append(str(e))
    con.commit()

    # 3. contagem por tabela
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    nomes = [r[0] for r in cur.fetchall()]
    contagem = []
    total_linhas = 0
    for t in nomes:
        cur.execute(f'SELECT COUNT(*) FROM "{t}"')
        n = cur.fetchone()[0]
        total_linhas += n
        contagem.append({'tabela': t, 'linhas': n})
    con.close()

    return {
        'resumo': dados['resumo'],
        'banco': {
            'arquivo': str(db_path),
            'tabelas_criadas': tabelas_ok,
            'linhas_inseridas': linhas_ok,
            'total_linhas': total_linhas,
            'erros_ddl': len(erros_ddl),
            'erros_insert': len(erros_ins),
        },
        'contagem': contagem,
        'tabelas': dados['tabelas'],
    }


def ler_registros_tabela(db_path, tabela: str, limite: int = 100) -> dict:
    """Le os registros de uma tabela do banco SQLite (colunas + linhas).

    Se o banco nao existir, gera-o antes (com massa padrao) para ter os dados.
    O nome da tabela vem no formato SCHEMA.TABELA ou SCHEMA_TABELA.
    """
    import sqlite3
    import re as _re

    db_path = Path(db_path)
    # nome fisico no SQLite usa underscore no lugar do ponto
    nome_fisico = tabela.replace('.', '_')
    # validacao simples do nome (evita injecao)
    if not _re.match(r'^[A-Za-z0-9_]+$', nome_fisico):
        raise ValueError('Nome de tabela invalido.')

    if not db_path.exists():
        raise FileNotFoundError('Banco ainda nao gerado. Gere o banco local primeiro.')

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    # confere se a tabela existe
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nome_fisico,))
    if not cur.fetchone():
        con.close()
        raise ValueError(f'Tabela {nome_fisico} nao encontrada no banco.')

    cur.execute(f'SELECT * FROM "{nome_fisico}" LIMIT {int(limite)}')
    colunas = [d[0] for d in cur.description]
    linhas = [list(r) for r in cur.fetchall()]
    cur.execute(f'SELECT COUNT(*) FROM "{nome_fisico}"')
    total = cur.fetchone()[0]
    con.close()

    return {
        'tabela': tabela,
        'tabela_fisica': nome_fisico,
        'colunas': colunas,
        'linhas': linhas,
        'total': total,
        'exibindo': len(linhas),
    }
