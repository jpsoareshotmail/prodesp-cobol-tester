"""Teste end-to-end: parse copybook -> DDL -> massa -> cria e popula SQLite.
Prova que o que a ferramenta gera e executavel de fato.
Roda da raiz: py -m tooling._test_e2e
"""
import re
import sqlite3

from tooling.copybook_parser import parse_file
from tooling.ddl_generator import gerar_ddl
from tooling.data_generator import gerar_inserts

CPY = 'entregas/copybook-Amostragem POC  - Fontes Convertidos/Originais/MAPA_COFI04.cpy'
TABELA = 'COFI04DS'


def ddl_para_sqlite(ddl: str) -> str:
    """Converte tipos DB2 para tipos que o SQLite entende (validacao local)."""
    ddl = re.sub(r'\bDECIMAL\(\d+(,\d+)?\)', 'NUMERIC', ddl)
    ddl = re.sub(r'\bCHAR\(\d+\)', 'TEXT', ddl)
    ddl = re.sub(r'\bVARCHAR\(\d+\)', 'TEXT', ddl)
    ddl = ddl.replace('SMALLINT', 'INTEGER').replace('BIGINT', 'INTEGER')
    return ddl


campos = parse_file(CPY)
ddl = gerar_ddl(TABELA, campos)
inserts = gerar_inserts(TABELA, campos, n=10)

con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.executescript(ddl_para_sqlite(ddl))
print('OK: CREATE TABLE executado no SQLite')

n_ins = 0
for stmt in inserts.strip().split('\n'):
    cur.execute(stmt)
    n_ins += 1
con.commit()
print(f'OK: {n_ins} INSERTs executados')

cur.execute(f'SELECT COUNT(*) FROM {TABELA}')
total = cur.fetchone()[0]
cur.execute(f'SELECT COUNT(*) FROM {TABELA} WHERE CO04CONF IS NULL')
nulos = cur.fetchone()[0]
print(f'OK: {total} linhas na tabela, {nulos} com CO04CONF NULL (coluna nullable)')
print('\nAmostra (3 primeiras linhas, colunas selecionadas):')
cur.execute(f'SELECT C_1ST_CO04PLAC, CO04MUNI, CO04CONF, CO04CGCF FROM {TABELA} LIMIT 3')
for row in cur.fetchall():
    print('   ', row)
con.close()
print('\n=== E2E OK: copybook -> DDL -> massa -> banco executavel ===')
