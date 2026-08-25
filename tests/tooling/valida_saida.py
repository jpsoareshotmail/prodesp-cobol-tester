"""Valida que schema.sql + massa.sql geram um banco SQLite executavel."""
import re
import sqlite3
from pathlib import Path

OUT = Path('saida_estrutura')


def db2_para_sqlite(sql: str) -> str:
    sql = re.sub(r'\bDECIMAL\(\d+(,\d+)?\)', 'NUMERIC', sql)
    sql = re.sub(r'\b(CHAR|VARCHAR)\(\d+\)', 'TEXT', sql)
    sql = sql.replace('SMALLINT', 'INTEGER').replace('BIGINT', 'INTEGER')
    # SQLite nao aceita schema.tabela em CREATE; remove o prefixo de schema
    sql = re.sub(r'CREATE TABLE\s+[A-Z0-9_]+\.', 'CREATE TABLE ', sql)
    sql = re.sub(r'INSERT INTO\s+[A-Z0-9_]+\.', 'INSERT INTO ', sql)
    return sql


schema = db2_para_sqlite((OUT / 'schema.sql').read_text(encoding='utf-8'))
massa = db2_para_sqlite((OUT / 'massa.sql').read_text(encoding='utf-8'))

con = sqlite3.connect(':memory:')
cur = con.cursor()

# executa CREATE TABLEs
tabelas_ok = 0
erros_ddl = []
for stmt in re.split(r';\s*\n', schema):
    s = stmt.strip()
    if not s.upper().startswith('CREATE TABLE'):
        continue
    try:
        cur.execute(s + ';')
        tabelas_ok += 1
    except Exception as e:
        erros_ddl.append(str(e))

# executa INSERTs
ins_ok = 0
erros_ins = []
for stmt in massa.splitlines():
    s = stmt.strip()
    if not s.upper().startswith('INSERT'):
        continue
    try:
        cur.execute(s)
        ins_ok += 1
    except Exception as e:
        if len(erros_ins) < 5:
            erros_ins.append(str(e))
con.commit()

print(f'CREATE TABLE executados OK : {tabelas_ok}')
print(f'  erros DDL: {len(erros_ddl)}')
for e in erros_ddl[:5]:
    print('    -', e)
print(f'INSERTs executados OK      : {ins_ok}')
print(f'  erros INSERT: {len(erros_ins)}')
for e in erros_ins:
    print('    -', e)

# contagem por algumas tabelas
cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 3")
for (t,) in cur.fetchall():
    cur.execute(f'SELECT COUNT(*) FROM "{t}"')
    print(f'  {t}: {cur.fetchone()[0]} linhas')
con.close()
