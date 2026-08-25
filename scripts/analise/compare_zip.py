import zipfile
import hashlib
from pathlib import Path

z = Path('entregas/Amostragem POC  - Fontes Convertidos.zip')
# Pasta ja descompactada anteriormente
existente = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos')

# 1. Nomes/hashes dentro do zip
zip_files = {}  # nome_relativo -> md5
with zipfile.ZipFile(z) as zf:
    for info in zf.infolist():
        if info.is_dir():
            continue
        data = zf.read(info.filename)
        zip_files[info.filename.replace('\\', '/')] = hashlib.md5(data).hexdigest()

# 2. Nomes/hashes da pasta existente
disk_files = {}
if existente.exists():
    for f in existente.rglob('*'):
        if f.is_file():
            rel = f.relative_to(existente).as_posix()
            disk_files[rel] = hashlib.md5(f.read_bytes()).hexdigest()

zip_set = set(zip_files)
disk_set = set(disk_files)

somente_zip = zip_set - disk_set
somente_disk = disk_set - zip_set
comuns = zip_set & disk_set
diferentes = [n for n in comuns if zip_files[n] != disk_files[n]]

print(f'Arquivos no ZIP novo         : {len(zip_set)}')
print(f'Arquivos na pasta existente  : {len(disk_set)}')
print(f'Em comum (mesmo nome)        : {len(comuns)}')
print()
print(f'NOVOS (so no zip, nao tinhamos): {len(somente_zip)}')
for n in sorted(somente_zip):
    print(f'   + {n}')
print()
print(f'CONTEUDO DIFERENTE (mesmo nome, bytes diferentes): {len(diferentes)}')
for n in sorted(diferentes):
    print(f'   ~ {n}')
print()
print(f'So na pasta existente (nao no zip): {len(somente_disk)}')
for n in sorted(somente_disk):
    print(f'   - {n}')
