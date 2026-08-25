import re
from pathlib import Path

BASE = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos')
CONV = BASE / 'Convertidos'
ORIG = BASE / 'Originais'

def ler(f):
    return f.read_text(encoding='latin-1', errors='ignore')

def coleta_copy(pasta, exts=None):
    refs = {}
    for f in pasta.iterdir():
        if not f.is_file():
            continue
        if exts and f.suffix.lower() not in exts and f.suffix != '':
            pass
        txt = ler(f)
        # Nos originais Unisys o include pode ser COPY "MAPA/NOME" ou COPY NOME
        for cp in re.findall(r'\bCOPY\s+"?[\w/]*?([\w-]+)"?\s*\.', txt, re.IGNORECASE):
            refs.setdefault(cp.upper(), set()).add(f.name)
        # tambem forma simples COPY NOME
        for cp in re.findall(r'\bCOPY\s+([A-Z0-9][\w-]+)', txt, re.IGNORECASE):
            refs.setdefault(cp.upper(), set()).add(f.name)
    return refs

# So programas em cada pasta
def eh_programa(f):
    t = ler(f).upper()
    return 'PROGRAM-ID' in t or 'IDENTIFICATION DIVISION' in t

conv_refs = {}
for f in CONV.iterdir():
    if f.is_file() and eh_programa(f):
        for cp in re.findall(r'\bCOPY\s+"?[\w/]*?([\w-]+)"?', ler(f), re.IGNORECASE):
            conv_refs.setdefault(cp.upper(), set()).add(f.name)

orig_refs = {}
for f in ORIG.iterdir():
    if f.is_file() and eh_programa(f):
        for cp in re.findall(r'\bCOPY\s+"?[\w/]*?([\w-]+)"?', ler(f), re.IGNORECASE):
            orig_refs.setdefault(cp.upper(), set()).add(f.name)

conv = set(conv_refs)
orig = set(orig_refs)

# arquivos presentes na entrega (nomes normalizados)
presentes = set()
for f in list(CONV.iterdir()) + list(ORIG.iterdir()):
    if f.is_file():
        n = f.stem.upper()
        if n.startswith('MAPA_'):
            n = n[5:]
        presentes.add(n)
        presentes.add(f.name.upper())

print('=== COPY referenciados ===')
print(f'Programas CONVERTIDOS referenciam: {len(conv)} copybooks distintos')
print(f'Programas ORIGINAIS (.C74) referenciam: {len(orig)} copybooks distintos')
print()
so_orig = sorted(orig - conv)
so_conv = sorted(conv - orig)
print(f'Referenciados SO nos ORIGINAIS (nao nos convertidos): {len(so_orig)}')
print('  ' + (', '.join(so_orig) if so_orig else '(nenhum)'))
print()
print(f'Referenciados SO nos CONVERTIDOS (nao nos originais): {len(so_conv)}')
print('  ' + (', '.join(so_conv) if so_conv else '(nenhum)'))
print()

# Faltantes considerando UNIAO (originais + convertidos)
uniao = conv | orig
faltam_uniao = sorted(uniao - presentes)
print('=== Considerando UNIAO (originais + convertidos) ===')
print(f'Total copybooks referenciados (uniao): {len(uniao)}')
print(f'Presentes na entrega: {len(uniao & presentes)}')
print(f'FALTANTES (uniao): {len(faltam_uniao)}')

# Diferenca em relacao a analise so-convertidos
faltam_conv = sorted(conv - presentes)
print()
print(f'FALTANTES so-convertidos: {len(faltam_conv)}')
novos = sorted(set(faltam_uniao) - set(faltam_conv))
print(f'Copybooks a mais que aparecem so por causa dos ORIGINAIS: {len(novos)}')
print('  ' + (', '.join(novos) if novos else '(nenhum)'))
