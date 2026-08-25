"""
Gerador de massa de dados sintetica a partir do modelo de campos do copybook.

Para cada campo elementar, gera valores validos conforme:
  - tipo/tamanho do PIC (do copybook, portanto fiel)
  - heuristica de dominio pelo nome (placa, chassi, cpf, cnpj, data, hora, ...)
  - nullable: parte das linhas recebe NULL nas colunas anulaveis
  - casos de borda: primeira e ultima linha exercitam limites (min/max, nulos)

Saidas:
  gerar_linhas(campos, n) -> lista de dicts {coluna: valor}
  gerar_inserts(table, campos, n) -> script INSERT ... VALUES ...;
"""
from __future__ import annotations

import random
from datetime import date, timedelta

from .copybook_parser import iter_elementary
from .ddl_generator import _col_name, sql_type


_UF = ['SP', 'RJ', 'MG', 'PR', 'RS', 'BA', 'SC', 'GO', 'PE', 'CE']


def _dominio(nome: str) -> str | None:
    u = nome.upper()
    if 'PLACA' in u or u.endswith('PLAC'):
        return 'placa'
    if 'CHAS' in u or 'CHASSI' in u:
        return 'chassi'
    if 'CPF' in u:
        return 'cpf'
    if 'CGC' in u or 'CNPJ' in u:
        return 'cnpj'
    if 'RENAV' in u:
        return 'renavam'
    if '-DT-' in u or 'DATA' in u or u.endswith('DT'):
        return 'data'
    if '-HR-' in u or 'HORA' in u:
        return 'hora'
    if 'MUNI' in u or 'MUNICIPIO' in u:
        return 'municipio'
    if 'UF' in u or 'ESTADO' in u:
        return 'uf'
    if 'NOME' in u:
        return 'nome'
    if 'ANO' in u:
        return 'ano'
    return None


def _gera_placa(rng):
    return f'{rng.choice(["ABC","DEF","GHI","XYZ"])}{rng.randint(1000,9999)}'


def _gera_num(digitos, rng, borda=None):
    if borda == 'min':
        return 0
    if borda == 'max':
        return int('9' * digitos)
    return rng.randint(0, int('9' * digitos))


def _valor_campo(campo, rng, borda=None):
    pic = campo.pic
    dom = _dominio(campo.name)

    if pic.category == 'alfanumerico':
        n = max(pic.length, 1)
        if borda == 'min':
            return ''
        if dom == 'placa':
            return _gera_placa(rng)[:n].ljust(min(n, 7))
        if dom == 'chassi':
            base = ''.join(rng.choice('ABCDEFGHJKLMNPRSTUVWXYZ0123456789') for _ in range(n))
            return base[:n]
        if dom == 'uf':
            return rng.choice(_UF)[:n]
        if dom == 'nome':
            nomes = ['SILVA', 'SOUZA', 'OLIVEIRA', 'SANTOS', 'PEREIRA', 'COSTA']
            return rng.choice(nomes)[:n].ljust(min(n, 6))
        if borda == 'max':
            return 'Z' * n
        # texto generico
        return ('T' + str(rng.randint(0, 10**min(n-1, 6))))[:n]

    if pic.category == 'numerico':
        i, d = pic.integer_digits, pic.decimal_digits
        if dom == 'cpf':
            return _gera_num(min(i, 11), rng, borda)
        if dom == 'cnpj':
            return _gera_num(min(i, 14), rng, borda)
        if dom == 'renavam':
            return _gera_num(min(i, 11), rng, borda)
        if dom == 'municipio':
            return _gera_num(min(i, 5), rng, borda) or 3550308  # Sao Paulo
        if dom == 'ano':
            if borda == 'min':
                return 1990
            if borda == 'max':
                return 2026
            return rng.randint(1990, 2026)
        if dom == 'data':
            base = date(2020, 1, 1)
            dt = base + timedelta(days=rng.randint(0, 2000))
            return int(dt.strftime('%Y%m%d'))  # AAAAMMDD
        if dom == 'hora':
            return rng.randint(0, 235959)
        if d > 0:
            inteiro = _gera_num(i, rng, borda)
            frac = _gera_num(d, rng, borda)
            return float(f'{inteiro}.{str(frac).zfill(d)}')
        return _gera_num(i, rng, borda)

    return None


def gerar_linhas(campos: list, n: int = 10, seed: int = 42) -> list:
    rng = random.Random(seed)
    elementares = [(tr, c) for tr, c in iter_elementary(campos)]
    linhas = []
    vistos_ordem = []
    # resolver nomes de coluna (mesma logica do DDL, com desambiguacao)
    nomes_col = []
    usados = set()
    for tr, c in elementares:
        col = _col_name(c.name)
        if col in usados:
            k = 2
            while f'{col}_{k}' in usados:
                k += 1
            col = f'{col}_{k}'
        usados.add(col)
        nomes_col.append(col)

    for r in range(n):
        borda = 'min' if r == 0 else ('max' if r == 1 else None)
        linha = {}
        for (tr, c), col in zip(elementares, nomes_col):
            # colunas nullable recebem NULL em ~20% das linhas (e sempre na linha 2 de borda)
            if c.nullable and (r == 2 or rng.random() < 0.2):
                linha[col] = None
            else:
                linha[col] = _valor_campo(c, rng, borda)
        linhas.append(linha)
    return linhas


def _sql_literal(valor) -> str:
    if valor is None:
        return 'NULL'
    if isinstance(valor, (int, float)):
        return str(valor)
    esc = str(valor).replace("'", "''")
    return f"'{esc}'"


def gerar_inserts(table_name: str, campos: list, n: int = 10,
                  schema: str = None, seed: int = 42) -> str:
    linhas = gerar_linhas(campos, n=n, seed=seed)
    if not linhas:
        return f'-- (sem colunas para {table_name})'
    cols = list(linhas[0].keys())
    full = f'{schema}.{table_name}' if schema else table_name
    col_list = ', '.join(cols)
    out = []
    for linha in linhas:
        vals = ', '.join(_sql_literal(linha[c]) for c in cols)
        out.append(f'INSERT INTO {full} ({col_list}) VALUES ({vals});')
    return '\n'.join(out)


def gerar_de_arquivo(path, table_name: str = None, n: int = 10, schema: str = None) -> str:
    from pathlib import Path
    from .copybook_parser import parse_file
    campos = parse_file(path)
    if table_name is None:
        table_name = Path(path).stem.replace('MAPA_', '').upper()
    return gerar_inserts(table_name, campos, n=n, schema=schema)
