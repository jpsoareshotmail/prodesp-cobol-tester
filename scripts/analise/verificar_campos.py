import re
from pathlib import Path

BASE = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos')
arquivos = [f for f in BASE.rglob('*') if f.is_file() and f.suffix.lower() != '.xlsx']

def ler(f):
    return f.read_text(encoding='latin-1', errors='ignore')

corpus = {f.relative_to(BASE).as_posix(): ler(f) for f in arquivos}

# 1. Conjunto de TODOS os nomes de dados DEFINIDOS em qualquer arquivo entregue
#    Definicao = "<nivel 01-49> <nome> ..."
defre = re.compile(r'^\s*(\d\d)\s+([A-Z0-9][\w-]+)', re.IGNORECASE | re.MULTILINE)
definidos = set()
for rel, c in corpus.items():
    for m in defre.finditer(c):
        definidos.add(m.group(2).upper().rstrip('.'))
print(f'Total de nomes de dados DEFINIDOS em toda a entrega: {len(definidos)}')

# 2. Host-variables usadas nos programas (referencia a campos de dataset via :var)
prog_files = []
for rel, c in corpus.items():
    if 'PROGRAM-ID' in c.upper() or 'IDENTIFICATION DIVISION' in c.upper():
        prog_files.append(rel)

host_vars = set()
for rel in prog_files:
    host_vars |= set(re.findall(r':([A-Z0-9][\w-]+)', corpus[rel].upper()))
host_vars = {h.rstrip('.') for h in host_vars if len(h) >= 4}
print(f'Total host-variables (:var) usadas em TODOS os programas: {len(host_vars)}')

# 3. Quantas dessas host-vars NAO estao definidas em lugar nenhum da entrega
nao_def = sorted(h for h in host_vars if h not in definidos)
sim_def = sorted(h for h in host_vars if h in definidos)
print(f'\nHost-vars DEFINIDAS na entrega: {len(sim_def)}')
print(f'Host-vars NAO DEFINIDAS (viriam dos copybooks faltantes): {len(nao_def)}')

print('\nExemplos de campos usados nos programas mas NAO definidos na entrega:')
for e in nao_def[:40]:
    print(f'  {e}')

# 4. Foco: campos dos datasets criticos (prefixos comuns)
#    Vamos agrupar os nao-definidos por prefixo (3 letras) para ver as familias
from collections import Counter
pref = Counter(h.split('-')[0] for h in nao_def)
print('\nPrefixos mais comuns entre os campos NAO definidos (familia -> qtd):')
for p, q in pref.most_common(20):
    print(f'  {p:<12} {q}')
