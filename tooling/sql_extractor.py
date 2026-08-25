"""
Extrator de metadados SQL dos programas COBOL convertidos.

Varre um programa e extrai, de cada bloco EXEC SQL ... END-EXEC:
  - tabelas (schema.tabela) das clausulas FROM / INTO / UPDATE / DELETE FROM
  - colunas de cada tabela (lista do SELECT nos DECLARE CURSOR)
  - colunas-chave candidatas (das clausulas WHERE e ORDER BY)
  - mapeamento coluna <-> host-variable (dos FETCH ... INTO)

Isso permite gerar a DDL com os NOMES DE COLUNA SQL reais que o programa usa,
e casar cada coluna com o campo do copybook para obter o tipo/tamanho fiel.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class TableInfo:
    schema: str
    name: str
    columns: list = field(default_factory=list)     # ordem de aparicao no SELECT
    keys: set = field(default_factory=set)           # colunas em WHERE/ORDER BY
    col_to_hostvar: dict = field(default_factory=dict)  # COLUNA_SQL -> HOST-VAR
    programs: set = field(default_factory=set)

    @property
    def full_name(self):
        return f'{self.schema}.{self.name}' if self.schema else self.name


_EXEC_RE = re.compile(r'EXEC\s+SQL(.*?)END-EXEC', re.IGNORECASE | re.DOTALL)
_FROM_RE = re.compile(r'\bFROM\s+([A-Z0-9_]+)\.([A-Z0-9_]+)', re.IGNORECASE)
_INTO_TAB_RE = re.compile(r'\bINSERT\s+INTO\s+([A-Z0-9_]+)\.([A-Z0-9_]+)', re.IGNORECASE)
_UPD_RE = re.compile(r'\bUPDATE\s+([A-Z0-9_]+)\.([A-Z0-9_]+)', re.IGNORECASE)
_SELECT_RE = re.compile(r'\bSELECT\b(.*?)\bFROM\b', re.IGNORECASE | re.DOTALL)
_WHERE_RE = re.compile(r'\bWHERE\b(.*?)(?:\bORDER\s+BY\b|\bGROUP\s+BY\b|\bFETCH\b|\bFOR\s+UPDATE\b|$)', re.IGNORECASE | re.DOTALL)
_ORDER_RE = re.compile(r'\bORDER\s+BY\b(.*?)(?:\bFETCH\b|\bFOR\s+UPDATE\b|$)', re.IGNORECASE | re.DOTALL)
_FETCH_RE = re.compile(r'\bFETCH\s+[\w-]+\s+INTO\b(.*?)$', re.IGNORECASE | re.DOTALL)
_COL_TOKEN = re.compile(r'[A-Z][A-Z0-9_]+', re.IGNORECASE)


def _limpa(texto: str) -> str:
    """Remove comentarios COBOL (col 7 = '*') e marcadores *GOT*."""
    out = []
    for l in texto.splitlines():
        if len(l) >= 7 and l[6] == '*':
            continue
        if l.lstrip().startswith('*'):
            continue
        out.append(re.sub(r'\*\w+\*\s*$', '', l))
    return '\n'.join(out)


def _split_colunas(select_body: str) -> list:
    """Extrai colunas de uma lista SELECT (separadas por virgula ou linha)."""
    cols = []
    for parte in re.split(r'[,\n]', select_body):
        p = parte.strip()
        if not p:
            continue
        # pega o primeiro identificador (ignora funcoes/aliases simples)
        m = _COL_TOKEN.match(p)
        if m:
            tok = m.group(0).upper()
            if tok not in ('DISTINCT', 'ALL'):
                cols.append(tok)
    return cols


def extrair_tabelas(texto: str, programa: str = '') -> dict:
    """Retorna {full_name: TableInfo} do programa."""
    txt = _limpa(texto)
    tabelas = {}

    def get(schema, name):
        key = f'{schema}.{name}'.upper()
        if key not in tabelas:
            tabelas[key] = TableInfo(schema=schema.upper(), name=name.upper())
        if programa:
            tabelas[key].programs.add(programa)
        return tabelas[key]

    # 1a passada: mapear nome-do-cursor -> tabela e colunas (DECLARE CURSOR)
    cursor_tab = {}   # nome_cursor -> full_name
    for m in _EXEC_RE.finditer(txt):
        bloco = m.group(1)
        dm = re.search(r'DECLARE\s+([\w-]+)\s+CURSOR', bloco, re.IGNORECASE)
        fmd = _FROM_RE.search(bloco)
        if dm and fmd:
            cursor_tab[dm.group(1).upper()] = f'{fmd.group(1)}.{fmd.group(2)}'.upper()

    for m in _EXEC_RE.finditer(txt):
        bloco = m.group(1)

        # tabela principal
        fm = _FROM_RE.search(bloco)
        im = _INTO_TAB_RE.search(bloco)
        um = _UPD_RE.search(bloco)
        alvo = None
        if fm:
            alvo = get(fm.group(1), fm.group(2))
        elif im:
            alvo = get(im.group(1), im.group(2))
        elif um:
            alvo = get(um.group(1), um.group(2))
        if alvo is None:
            continue

        # colunas do SELECT
        sm = _SELECT_RE.search(bloco)
        if sm:
            for c in _split_colunas(sm.group(1)):
                if c not in alvo.columns:
                    alvo.columns.append(c)

        # chaves (WHERE / ORDER BY)
        wm = _WHERE_RE.search(bloco)
        if wm:
            for c in re.findall(r'([A-Z][A-Z0-9_]+)\s*[=<>]', wm.group(1), re.IGNORECASE):
                alvo.keys.add(c.upper())
        om = _ORDER_RE.search(bloco)
        if om:
            for c in _split_colunas(om.group(1)):
                alvo.keys.add(c)

    _mapear_fetch(txt, tabelas)
    return tabelas


def _mapear_fetch(txt: str, tabelas: dict):
    """Associa FETCH <cursor> INTO :hv,... com a tabela do cursor e casa
    coluna<->host-var pela ordem."""
    # cursor -> colunas
    cursor_cols = {}
    for m in _EXEC_RE.finditer(txt):
        bloco = m.group(1)
        dm = re.search(r'DECLARE\s+([\w-]+)\s+CURSOR', bloco, re.IGNORECASE)
        fmd = _FROM_RE.search(bloco)
        sm = _SELECT_RE.search(bloco)
        if dm and fmd and sm:
            cursor_cols[dm.group(1).upper()] = (
                f'{fmd.group(1)}.{fmd.group(2)}'.upper(),
                _split_colunas(sm.group(1)),
            )
    for m in _EXEC_RE.finditer(txt):
        bloco = m.group(1)
        fm = re.search(r'FETCH\s+([\w-]+)\s+INTO\b(.*)$', bloco, re.IGNORECASE | re.DOTALL)
        if not fm:
            continue
        cur = fm.group(1).upper()
        if cur not in cursor_cols:
            continue
        full, cols = cursor_cols[cur]
        if full not in tabelas:
            continue
        hostvars = re.findall(r':([A-Z0-9][\w-]*)', fm.group(2), re.IGNORECASE)
        for col, hv in zip(cols, hostvars):
            tabelas[full].col_to_hostvar[col] = hv.upper()


def extrair_de_arquivo(path, programa: str = None) -> dict:
    from pathlib import Path
    p = Path(path)
    if programa is None:
        programa = p.name
    return extrair_tabelas(p.read_text(encoding='latin-1', errors='ignore'), programa)
