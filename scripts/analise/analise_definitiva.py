import re
from pathlib import Path

CONV = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Convertidos')

arquivos = sorted([f for f in CONV.iterdir() if f.is_file()])

def ler(f):
    return f.read_text(encoding='latin-1', errors='ignore')

# 1. Classificar cada arquivo por CONTEUDO
programas = []   # tem PROGRAM-ID
copybooks = []   # nao tem PROGRAM-ID, comeca em nivel de dado
for f in arquivos:
    txt = ler(f).upper()
    if 'PROGRAM-ID' in txt or 'IDENTIFICATION DIVISION' in txt:
        programas.append(f.name)
    else:
        copybooks.append(f.name)

print('========================================================')
print('PARTE 1 - Classificacao dos 56 arquivos por CONTEUDO')
print('========================================================')
print(f'PROGRAMAS ({len(programas)}):')
print('  ' + ', '.join(programas))
print()
print(f'COPYBOOKS presentes na pasta ({len(copybooks)}):')
print('  ' + ', '.join(copybooks))
print()

# 2. Coletar TODOS os COPY referenciados pelos programas + em qual fonte
copy_refs = {}
for f in arquivos:
    if f.name not in programas:
        continue
    txt = ler(f)
    for cp in re.findall(r'\bCOPY\s+([\w-]+)', txt, re.IGNORECASE):
        copy_refs.setdefault(cp.upper(), set()).add(f.name)

todos = set(copy_refs)

# 3. O que EXISTE na pasta (qualquer arquivo, nome = copybook)
presentes_pasta = set(f.name.upper() for f in arquivos)

# 4. Faltantes de verdade = referenciados mas NAO presentes na pasta
faltantes = sorted(todos - presentes_pasta)
recebidos_ref = sorted(todos & presentes_pasta)

print('========================================================')
print('PARTE 2 - COPY referenciados x presentes na pasta')
print('========================================================')
print(f'Total COPY distintos referenciados pelos programas: {len(todos)}')
print(f'Referenciados E presentes na pasta (recebidos): {len(recebidos_ref)}')
print('  ' + ', '.join(recebidos_ref))
print()
print(f'FALTANDO DE VERDADE (referenciados mas ausentes): {len(faltantes)}')
print()
for cp in faltantes:
    fontes = ', '.join(sorted(copy_refs[cp]))
    print(f'  {cp}  <- {fontes}')
