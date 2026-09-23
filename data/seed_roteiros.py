"""
Semeia o banco SQLite local com os dados dos Roteiros de Teste (Primeiro
Emplacamento), para que os FETCH/SELECT reais dos programas (via ponte
pdsqlbridge) encontrem registros e o programa calcule um resultado de negocio.

Estrategia: para cada cenario do roteiro (chassi/placa/CPF/CNPJ) e para cada
tabela que tenha alguma coluna de chave (CHASSI/PLACA/CPF/CGC), insere UMA
linha preenchendo:
  - colunas de chave -> com o valor do cenario (chassi, placa derivada, CPF/CNPJ)
  - demais colunas NOT NULL -> default por tipo (0 p/ numerico, espaco p/ texto)
Assim um WHERE por qualquer dessas chaves casa. Idempotente (limpa e reinsere
as linhas de roteiro identificadas por um ROWID_ com prefixo 'RT').
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

# placa Mercosul de teste usada nos cenarios (o roteiro nao tem placa real -
# e' o processo de PRIMEIRA emissao; usamos uma placa ficticia consistente).
_PLACA = {
    '9C2GAA1SNSP772009': 'ABC1D23',
    '9BMGAA1SNSP772016': 'DEF2E45',
    '9C2GAA1SNSP772010': 'GHI3F67',
}


def _cenarios():
    try:
        from data.roteiros_teste import get_roteiros
    except ImportError:
        from roteiros_teste import get_roteiros  # type: ignore
    out = []
    for r in get_roteiros():
        dt = r.get('dados_teste', {})
        chassi = (dt.get('chassi') or '').strip()
        if not chassi:
            continue
        out.append({
            'chassi': chassi,
            'placa': _PLACA.get(chassi, 'AAA0A00'),
            'cpf': (dt.get('cpf') or '').strip(),
            'cnpj': (dt.get('cnpj') or '').strip(),
            'cenario': r.get('cenario', ''),
        })
    return out


def _valor_chave(coluna: str, cen: dict) -> str | None:
    """Valor do cenario para uma coluna de chave, conforme o que ela representa."""
    u = coluna.upper()
    if 'CHASSI' in u:
        return cen['chassi']
    if 'PLACA_MERC' in u or u.endswith('PLACA_MERC'):
        return cen['placa']
    if 'PLACA' in u:
        return cen['placa']
    # CPF/CGC: usa CPF se houver, senao CNPJ
    if 'CPF' in u or 'CGC' in u or 'CNPJ' in u:
        return cen['cpf'] or cen['cnpj'] or None
    return None


def _default_por_tipo(tipo: str):
    """Default seguro para uma coluna NOT NULL sem valor de cenario."""
    t = (tipo or '').upper()
    if any(x in t for x in ('INT', 'NUM', 'DEC', 'REAL', 'FLOA', 'DOUB')):
        return 0
    return ' '   # texto: um espaco (nao vazio, evita ambiguidade)


# Colunas com valor FIXO conhecido para as linhas de roteiro, alem da chave de
# busca - necessario quando a consulta do programa usa chave COMPOSTA e o
# outro campo tem um valor especifico que a injecao de entrada forca.
# Ex: OGAA920D consulta TAXADS por (TAX_TIPO=IN-COD-SERVICO, TAX_CPF); a
# injecao forca IN-COD-SERVICO=17, entao TAX_TIPO das linhas semeadas = 17.
_COLUNAS_FIXAS = {
    'TAX_TIPO': 17,
}


def semear(db_path: str) -> dict:
    """Semeia o banco. Retorna estatisticas {tabelas, linhas}."""
    db = Path(db_path)
    if not db.exists():
        return {'erro': 'banco nao existe', 'tabelas': 0, 'linhas': 0}
    con = sqlite3.connect(str(db))
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [r[0] for r in cur.fetchall()]
    cens = _cenarios()

    n_tab = 0
    n_lin = 0
    for t in tabelas:
        cur.execute('PRAGMA table_info("%s")' % t)
        info = cur.fetchall()   # (cid, name, type, notnull, dflt, pk)
        cols = [(c[1], c[2], c[3], c[1] == 'ROWID_' or c[5]) for c in info]  # nome,tipo,notnull,ehchave-rowid
        nomes = [c[0] for c in cols]
        # so' semeia tabelas com alguma coluna de chave de busca
        tem_chave = any(any(k in c.upper() for k in ('CHASSI', 'PLACA', 'CPF', 'CGC', 'CNPJ')) for c in nomes)
        if not tem_chave:
            continue

        # remove linhas de roteiro anteriores (idempotente)
        try:
            cur.execute('DELETE FROM "%s" WHERE ROWID_ LIKE \'RT%%\'' % t)
        except Exception:
            pass

        for i, cen in enumerate(cens):
            valores = []
            colnames = []
            for nome, tipo, notnull, is_pk in cols:
                colnames.append(nome)
                if nome == 'ROWID_':
                    valores.append('RT%s%d' % (t[:6], i))
                    continue
                vchave = _valor_chave(nome, cen)
                if nome.upper() in _COLUNAS_FIXAS:
                    valores.append(_COLUNAS_FIXAS[nome.upper()])
                elif vchave is not None:
                    valores.append(vchave)
                elif notnull:
                    valores.append(_default_por_tipo(tipo))
                else:
                    valores.append(None)
            ph = ', '.join('?' for _ in colnames)
            cols_sql = ', '.join('"%s"' % c for c in colnames)
            try:
                cur.execute('INSERT INTO "%s" (%s) VALUES (%s)' % (t, cols_sql, ph), valores)
                n_lin += 1
            except Exception:
                pass
        n_tab += 1

    con.commit()
    con.close()
    return {'tabelas': n_tab, 'linhas': n_lin, 'cenarios': len(cens)}


if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv) > 1 else 'saida_estrutura/prodesp_teste.db'
    print(semear(p))
