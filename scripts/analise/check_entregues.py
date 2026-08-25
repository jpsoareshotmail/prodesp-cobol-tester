import re
from pathlib import Path

CONV = Path('fontes_convertidos/Convertidos')
ENTREGUE_CONV = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Convertidos')
ENTREGUE_ORIG = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Originais')
FALT = Path('fontes_faltanters')

# 1. Todos COPY referenciados (com as fontes que os usam)
copy_refs = {}
for f in sorted(CONV.iterdir()):
    if not f.is_file():
        continue
    txt = f.read_text(encoding='latin-1', errors='ignore')
    for cp in set(re.findall(r'COPY\s+([\w-]+)', txt)):
        copy_refs.setdefault(cp.upper(), []).append(f.name)

todos = set(copy_refs.keys())

# 2. Recebidos da pasta entregue Convertidos (nome bate com COPY)
receb_conv = set(f.name.upper() for f in ENTREGUE_CONV.iterdir() if f.is_file()) & todos

# 3. Recebidos da pasta entregue Originais (MAPA_ e outros)
receb_orig = set()
for f in ENTREGUE_ORIG.iterdir():
    if f.is_file():
        n = f.stem.upper()
        if n.startswith('MAPA_'):
            n = n[5:]
        if n in todos:
            receb_orig.add(n)

# 4. Recebidos de fontes_faltanters
receb_falt = set()
if FALT.exists():
    for f in FALT.iterdir():
        if f.is_file():
            n = f.stem.upper()
            for pfx in ['SUP_', 'ZPF_LIB_', 'PF_', 'ZPF_']:
                if n.startswith(pfx):
                    n = n[len(pfx):]
            if n in todos:
                receb_falt.add(n)

recebidos = receb_conv | receb_orig | receb_falt
faltantes = todos - recebidos

print(f'Total COPY referenciados : {len(todos)}')
print(f'  Recebidos pasta Convertidos : {len(receb_conv)} -> {sorted(receb_conv)}')
print(f'  Recebidos pasta Originais   : {len(receb_orig)} -> {sorted(receb_orig)}')
print(f'  Recebidos fontes_faltanters : {len(receb_falt)} -> {sorted(receb_falt)}')
print(f'  TOTAL recebidos (unicos)    : {len(recebidos)}')
print(f'  FALTANTES                   : {len(faltantes)}')
