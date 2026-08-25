import re
from pathlib import Path

BASE = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos')
CONV = BASE / 'Convertidos'

def ler(f):
    return f.read_text(encoding='latin-1', errors='ignore')

def eh_programa(f):
    t = ler(f).upper()
    return 'PROGRAM-ID' in t or 'IDENTIFICATION DIVISION' in t

# Metodo antigo (so COPY NOME)
antigo = {}
# Metodo novo (inclui COPY "MAPA/NOME")
novo = {}
for f in CONV.iterdir():
    if not (f.is_file() and eh_programa(f)):
        continue
    txt = ler(f)
    for cp in re.findall(r'\bCOPY\s+([A-Z0-9][\w-]+)', txt, re.IGNORECASE):
        antigo.setdefault(cp.upper(), set()).add(f.name)
    for cp in re.findall(r'\bCOPY\s+"?[\w/]*?([\w-]+)"?', txt, re.IGNORECASE):
        novo.setdefault(cp.upper(), set()).add(f.name)

diff = sorted(set(novo) - set(antigo))
print(f'Metodo antigo: {len(antigo)} | Metodo novo: {len(novo)}')
print(f'Copybook(s) capturado(s) so pelo metodo novo: {diff}')
for cp in diff:
    print(f'  {cp} <- {sorted(novo[cp])}')
    # Mostrar a linha exata
    for fn in sorted(novo[cp]):
        for i, l in enumerate(ler(CONV/fn).splitlines(), 1):
            if re.search(r'COPY.*' + re.escape(cp), l, re.IGNORECASE) and cp.upper() in l.upper():
                print(f'      {fn}:{i}: {l.strip()}')
                break
