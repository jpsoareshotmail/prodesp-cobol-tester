"""
Analisa quais copybooks sao referenciados pelos fontes convertidos (via COPY)
e quais foram entregues na pasta de copybooks.
Lista os faltantes e em quais fontes cada um e referenciado.
"""
import re
from pathlib import Path

CONV = Path('fontes_convertidos/Convertidos')
ENTREGUES_DIR = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos')

# 1. Coletar todos os COPY referenciados e em quais fontes
copy_refs = {}  # {copybook: [lista de fontes]}
for f in sorted(CONV.iterdir()):
    if not f.is_file() or f.name.startswith('MAPA'):
        continue
    content = f.read_text(encoding='latin-1')
    copies = set(re.findall(r'COPY\s+(\w+)', content))
    for cp in copies:
        copy_refs.setdefault(cp, []).append(f.name)

# 2. Coletar copybooks entregues (nomes de arquivos, sem extensao/prefixo)
# IMPORTANTE: um arquivo entregue so conta como copybook recebido se seu nome
# corresponder a um COPY referenciado (senao e apenas o fonte do programa/mapa).
entregues = set()
for sub in ['Convertidos', 'Originais']:
    d = ENTREGUES_DIR / sub
    if d.exists():
        for f in d.iterdir():
            if f.is_file():
                name = f.stem
                # Normalizar: remover prefixo MAPA_, extensoes
                if name.startswith('MAPA_'):
                    name = name[5:]
                name = name.upper()
                # So conta se for de fato um copybook referenciado
                if name in {c.upper() for c in copy_refs}:
                    entregues.add(name)

# Tambem os que ja temos em cobol_build/copy que vieram de fontes_faltanters
faltanters_dir = Path('fontes_faltanters')
faltanters = set()
if faltanters_dir.exists():
    for f in faltanters_dir.iterdir():
        if f.is_file():
            name = f.stem
            for pfx in ['SUP_', 'ZPF_LIB_', 'PF_']:
                if name.startswith(pfx):
                    name = name[len(pfx):]
            faltanters.add(name.upper())

# 3. Determinar faltantes
total = sorted(copy_refs.keys())
recebidos = []
faltantes = []
for cp in total:
    if cp.upper() in entregues or cp.upper() in faltanters:
        recebidos.append(cp)
    else:
        faltantes.append(cp)

print(f'=== ANALISE DE COPYBOOKS ===')
print(f'Total referenciados nos fontes: {len(total)}')
print(f'Recebidos (entregues + fontes_faltanters): {len(recebidos)}')
print(f'FALTANTES: {len(faltantes)}')
print()
print(f'=== COPYBOOKS FALTANTES E ONDE SAO REFERENCIADOS ===')
print()
for cp in faltantes:
    fontes = copy_refs[cp]
    print(f'{cp} ({len(fontes)} fontes):')
    print(f'   {", ".join(fontes)}')
