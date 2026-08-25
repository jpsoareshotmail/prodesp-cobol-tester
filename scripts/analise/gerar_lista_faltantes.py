import re
import csv
from pathlib import Path
from collections import defaultdict

# Fonte da verdade: a pasta entregue pela Prodesp
CONV = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Convertidos')

arquivos = sorted([f for f in CONV.iterdir() if f.is_file()])

def ler(f):
    return f.read_text(encoding='latin-1', errors='ignore')

# 1. Classificar programas x copybooks por conteudo
programas = []
copybooks_pasta = []
for f in arquivos:
    txt = ler(f).upper()
    if 'PROGRAM-ID' in txt or 'IDENTIFICATION DIVISION' in txt:
        programas.append(f.name)
    else:
        copybooks_pasta.append(f.name)

# 2. Coletar todos COPY referenciados pelos programas
copy_refs = {}
for f in arquivos:
    if f.name not in programas:
        continue
    txt = ler(f)
    for cp in re.findall(r'\bCOPY\s+([\w-]+)', txt, re.IGNORECASE):
        copy_refs.setdefault(cp.upper(), set()).add(f.name)

todos = set(copy_refs)
presentes = set(f.name.upper() for f in arquivos)
faltantes = sorted(todos - presentes, key=lambda c: (-len(copy_refs[c]), c))
recebidos = sorted(todos & presentes)

def categoria(cp):
    if cp in ('WSGL', 'PDGL', 'WSGLDB', 'PDGLDB'):
        return '1-GLOBAL (base)'
    if cp.startswith('WSD') or cp.startswith('PDD'):
        return '2-DADOS/BANCO (WSD/PDD)'
    if cp.startswith('WSBLQ') or cp.startswith('PDBLQ'):
        return '3-BLOQUEIO'
    if cp.startswith('WSFUR') or cp.startswith('PDFUR'):
        return '4-FURTO'
    if cp.startswith('WSTAB') or cp.startswith('PDTAB'):
        return '5-TABELAS'
    if cp.startswith('WSADM') or cp.startswith('PDADM'):
        return '6-ADMINISTRACAO'
    if cp.startswith('WSALG'):
        return '7-ALGORITMO'
    if cp in ('COMS', 'COMSIN', 'COMSOUT', 'CONTSPC', 'CONTWORK', 'CONTPERF'):
        return '8-RUNTIME ONLINE'
    if cp in ('SEECDT00', 'SEECDTPD'):
        return '9-LIB DMS'
    return '9-OUTROS'

# CSV
with open('docs/analise/COPYBOOKS_FALTANTES.csv', 'w', newline='', encoding='utf-8-sig') as fp:
    w = csv.writer(fp, delimiter=';')
    w.writerow(['Copybook', 'Categoria', 'Qtd Fontes', 'Fontes que referenciam'])
    for cp in faltantes:
        w.writerow([cp, categoria(cp), len(copy_refs[cp]), ', '.join(sorted(copy_refs[cp]))])

# Copybooks da pasta que NAO sao referenciados por nenhum programa
nao_usados = sorted(set(copybooks_pasta) - {c for c in presentes if c in todos})
# so os copybooks (nao programas) que nao aparecem em copy_refs
nao_usados = [c for c in copybooks_pasta if c.upper() not in todos]

# Markdown
lines = []
lines.append('# Copybooks Faltantes - POC Prodesp')
lines.append('')
lines.append('Base da analise: pasta entregue pela Prodesp')
lines.append('"copybook-Amostragem POC - Fontes Convertidos/Convertidos".')
lines.append('')
lines.append(f'- Arquivos na pasta: **{len(arquivos)}** ({len(programas)} programas + {len(copybooks_pasta)} copybooks)')
lines.append(f'- COPY distintos referenciados pelos programas: **{len(todos)}**')
lines.append(f'- Recebidos (referenciados E presentes na pasta): **{len(recebidos)}**')
lines.append(f'- **FALTANTES (referenciados mas ausentes): {len(faltantes)}**')
lines.append('')
lines.append('## Copybooks presentes na pasta (14 - todos de tela/mapa)')
lines.append('')
lines.append('  ' + ', '.join(copybooks_pasta))
lines.append('')
if nao_usados:
    lines.append(f'**Observacao:** o(s) copybook(s) {", ".join(nao_usados)} esta(o) na pasta '
                 'mas nao e(sao) referenciado(s) por nenhum programa via COPY. '
                 'No caso de AUML01: os programas referenciam AUMI01 (com "I"), que NAO veio - '
                 'possivel divergencia de nome a confirmar com a Prodesp.')
    lines.append('')
lines.append('Lista de faltantes ordenada por criticidade (numero de fontes que dependem).')
lines.append('')

por_cat = defaultdict(list)
for cp in faltantes:
    por_cat[categoria(cp)].append(cp)

for cat in sorted(por_cat):
    lines.append(f'## {cat} ({len(por_cat[cat])} copybooks)')
    lines.append('')
    lines.append('| Copybook | Qtd Fontes | Fontes que referenciam |')
    lines.append('|----------|-----------|------------------------|')
    for cp in por_cat[cat]:
        fontes = ', '.join(sorted(copy_refs[cp]))
        lines.append(f'| {cp} | {len(copy_refs[cp])} | {fontes} |')
    lines.append('')

Path('docs/analise/COPYBOOKS_FALTANTES.md').write_text('\n'.join(lines), encoding='utf-8')

print(f'Arquivos na pasta : {len(arquivos)} ({len(programas)} prog + {len(copybooks_pasta)} copybooks)')
print(f'COPY referenciados: {len(todos)}')
print(f'Recebidos         : {len(recebidos)}')
print(f'FALTANTES         : {len(faltantes)}')
print(f'Copybook na pasta nao usado: {nao_usados}')
print()
print('Faltantes por categoria:')
for cat in sorted(por_cat):
    print(f'  {cat}: {len(por_cat[cat])}')
print()
print('Gerados: COPYBOOKS_FALTANTES.md e COPYBOOKS_FALTANTES.csv')
