"""
Runtime SQLite para os EXEC SQL dos programas COBOL convertidos.

Em vez de neutralizar o FETCH com "NOTFOUND", gera COBOL que monta um SELECT
com o valor da chave (host var do WHERE) e chama a ponte C (pdsqlbridge.dll,
funcao PDSQL_QRY) que consulta o banco SQLite local de verdade. As colunas
achadas voltam em slots de 40 chars e sao movidas para as host vars do INTO.

Fluxo:
  1. extrair_cursores(fonte)  -> {CURSOR: CursorInfo} com tabela fisica,
     colunas do SELECT, e as condicoes do WHERE (coluna = :host-var).
  2. gerar_fetch_cobol(cursor_info, hostvars_into) -> bloco COBOL que faz o
     SELECT real e popula as host vars.

Limites: SELECT simples (uma tabela, WHERE com '=' e host vars). Consultas
que o parser nao entende caem no comportamento antigo (NOTFOUND), sem quebrar.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


SLOT = 40  # largura de cada coluna no buffer de saida (igual ao C)


@dataclass
class CursorInfo:
    nome: str
    tabela_fisica: str                 # ex: DBDETRAN_NOVAPLACDS
    colunas: list = field(default_factory=list)     # colunas do SELECT (ordem)
    where: list = field(default_factory=list)        # [(coluna, host_var)] do WHERE


_EXEC_RE = re.compile(r'EXEC\s+SQL(.*?)END-EXEC', re.IGNORECASE | re.DOTALL)
_DECL_RE = re.compile(r'DECLARE\s+([\w-]+)\s+CURSOR', re.IGNORECASE)
_FROM_RE = re.compile(r'\bFROM\s+([A-Z0-9_]+)\.([A-Z0-9_]+)', re.IGNORECASE)
_SELECT_RE = re.compile(r'\bSELECT\b(.*?)\bFROM\b', re.IGNORECASE | re.DOTALL)
_WHERE_RE = re.compile(r'\bWHERE\b(.*?)(?:\bORDER\s+BY\b|\bGROUP\s+BY\b|\bFETCH\b|\bFOR\s+UPDATE\b|$)',
                       re.IGNORECASE | re.DOTALL)
_COL_TOKEN = re.compile(r'[A-Z][A-Z0-9_]+', re.IGNORECASE)
# condicao "COLUNA = :HOST-VAR" (ignora AND/OR ao redor)
_COND_RE = re.compile(r'([A-Z][A-Z0-9_]+)\s*=\s*:([A-Z0-9][\w-]*)', re.IGNORECASE)


def _limpa(texto: str) -> str:
    """Remove comentarios COBOL (col 7 = '*'/'/') e marcadores *GOT*/*GOX*."""
    out = []
    for l in texto.splitlines():
        if len(l) >= 7 and l[6] in ('*', '/'):
            continue
        if l.lstrip().startswith('*'):
            continue
        out.append(re.sub(r'\*\w+\*\s*$', '', l))
    return '\n'.join(out)


def _split_colunas(select_body: str) -> list:
    cols = []
    for parte in re.split(r'[,\n]', select_body):
        p = parte.strip()
        if not p:
            continue
        m = _COL_TOKEN.match(p)
        if m:
            tok = m.group(0).upper()
            if tok not in ('DISTINCT', 'ALL'):
                cols.append(tok)
    return cols


def extrair_cursores(fonte: str) -> dict:
    """Retorna {NOME_CURSOR: CursorInfo} a partir dos DECLARE CURSOR do fonte."""
    txt = _limpa(fonte)
    cursores = {}
    for m in _EXEC_RE.finditer(txt):
        bloco = m.group(1)
        dm = _DECL_RE.search(bloco)
        if not dm:
            continue
        fm = _FROM_RE.search(bloco)
        sm = _SELECT_RE.search(bloco)
        if not (fm and sm):
            continue
        nome = dm.group(1).upper()
        tabela_fisica = f'{fm.group(1)}_{fm.group(2)}'.upper()   # schema_tabela
        colunas = _split_colunas(sm.group(1))
        where = []
        wm = _WHERE_RE.search(bloco)
        if wm:
            for cond in _COND_RE.finditer(wm.group(1)):
                where.append((cond.group(1).upper(), cond.group(2).upper()))
        cursores[nome] = CursorInfo(nome=nome, tabela_fisica=tabela_fisica,
                                    colunas=colunas, where=where)
    return cursores


def _nome_cursor_do_fetch(texto_bloco_upper: str) -> str | None:
    m = re.search(r'FETCH\s+([\w-]+)\s+INTO', texto_bloco_upper, re.IGNORECASE)
    return m.group(1).upper() if m else None


def _hostvars_into(texto_bloco_upper: str) -> list:
    """Lista as host vars do INTO na ordem (ex: [':NPL-PLACA-X', ...] sem ':')."""
    m = re.search(r'INTO\b(.*)$', texto_bloco_upper, re.IGNORECASE | re.DOTALL)
    if not m:
        return []
    return [hv.upper() for hv in re.findall(r':([A-Z0-9][\w-]*)', m.group(1))]


def gerar_fetch_cobol(texto_bloco_upper: str, cursores: dict, ponto: str,
                      offset_var: str | None = None) -> str | None:
    """Gera o bloco COBOL que executa o SELECT real via ponte e popula as host
    vars do INTO. Retorna None se nao souber tratar (o chamador cai no NOTFOUND).

    offset_var: se dado (nome de um campo PIC 9(4)), usa PDSQL_QRYN com paginacao
    (para FETCH NEXT em loop). Senao usa PDSQL_QRY (primeira linha).
    """
    nome = _nome_cursor_do_fetch(texto_bloco_upper)
    if not nome or nome not in cursores:
        return None
    ci = cursores[nome]
    if not ci.colunas or not ci.tabela_fisica:
        return None

    into = _hostvars_into(texto_bloco_upper)
    if not into:
        return None

    # monta o SELECT: colunas na ordem do DECLARE, WHERE com os valores das
    # host vars (colocadas entre aspas via COBOL STRING em runtime).
    col_list = ', '.join(ci.colunas)
    sql_texto = 'SELECT %s FROM %s' % (col_list, ci.tabela_fisica)

    L = []
    L.append('           MOVE SPACES TO WS-PDSQL-SQL')
    L.append('           STRING')
    # 'partes' = lista de itens do STRING; literais longos sao fatiados em
    # pedacos curtos (<=50 chars) para nunca estourar a coluna 72 do COBOL.
    for pedaco in _fatiar_literal(sql_texto):
        L.append('             "%s"' % pedaco)
    if ci.where:
        for i, (coluna, hv) in enumerate(ci.where):
            prefixo = ' WHERE ' if i == 0 else ' AND '
            for pedaco in _fatiar_literal("%s%s = '" % (prefixo, coluna)):
                L.append('             "%s"' % pedaco)
            # valor da host var (campo COBOL) sem aspas COBOL, com TRIM:
            L.append('             FUNCTION TRIM(%s)' % _cobol_name(hv))
            L.append('             "\'"')
    L.append('             DELIMITED BY SIZE INTO WS-PDSQL-SQL')
    L.append('           END-STRING')

    # chama a ponte
    if offset_var:
        L.append('           MOVE %s TO WS-PDSQL-OFFSET' % offset_var)
        L.append('           CALL "PDSQL_QRYN" USING WS-PDSQL-SQL WS-PDSQL-OFFSET')
        L.append('                WS-PDSQL-OUT WS-PDSQL-STATUS')
    else:
        L.append('           CALL "PDSQL_QRY" USING WS-PDSQL-SQL')
        L.append('                WS-PDSQL-OUT WS-PDSQL-STATUS')

    # se OK, move cada slot para a host var do INTO (na ordem das colunas)
    L.append('           IF WS-PDSQL-STATUS = "OK"')
    L.append('               MOVE "OK" TO DMSTATUS-S')
    for idx, hv in enumerate(into):
        if idx >= len(ci.colunas):
            break
        L.append('               MOVE WS-PDSQL-SLOT(%d) TO %s' % (idx + 1, _cobol_name(hv)))
    L.append('           ELSE')
    L.append('               MOVE "NOTFOUND" TO DMSTATUS-S')
    L.append('           END-IF' + ponto)
    return '\n'.join(L)


def _cobol_name(hostvar: str) -> str:
    """Host var como aparece no COBOL (mantem hifens, remove ':')."""
    return hostvar.lstrip(':')


def _fatiar_literal(texto: str, tam: int = 50) -> list:
    """Quebra um texto em pedacos de ate 'tam' chars para caber num literal
    COBOL de formato fixo (indentacao ~13 + aspas + tam <= coluna 72). Cada
    pedaco vira um item "..." separado no STRING - a concatenacao remonta o
    texto inteiro. Aspas simples no texto sao dobradas nao (nao ha ' no SQL
    gerado por nos, exceto os delimitadores que ja saem separados)."""
    return [texto[i:i + tam] for i in range(0, len(texto), tam)] or ['']


def bloco_working_storage() -> str:
    """Campos de apoio para a ponte, injetados uma vez no WORKING-STORAGE."""
    return (
        '      * Campos de apoio ao runtime SQLite (ponte pdsqlbridge)\n'
        '       01  WS-PDSQL-SQL          PIC X(2000) VALUE SPACES.\n'
        '       01  WS-PDSQL-OUT.\n'
        '           05  WS-PDSQL-SLOT     OCCURS 40 TIMES PIC X(040).\n'
        '       01  WS-PDSQL-STATUS       PIC X(008) VALUE SPACES.\n'
        '       01  WS-PDSQL-OFFSET       PIC 9(004) VALUE 0.\n'
    )
