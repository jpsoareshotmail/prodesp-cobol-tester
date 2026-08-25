import zipfile
from pathlib import Path

z = Path('entregas/Amostragem POC  - Fontes Convertidos.zip')
with zipfile.ZipFile(z) as zf:
    names = zf.namelist()

print(f'Total entradas no zip: {len(names)}')
print()
for n in sorted(names):
    print(n)
