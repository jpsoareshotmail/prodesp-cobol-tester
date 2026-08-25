import zipfile
import re
from pathlib import Path

z = Path('entregas/Amostragem POC  - Fontes Convertidos.zip')

def classificar(nome, txt):
    up = txt.upper()
    tem_id_div = 'IDENTIFICATION DIVISION' in up or 'PROGRAM-ID' in up
    tem_proc_div = 'PROCEDURE DIVISION' in up
    tem_ws_div = 'WORKING-STORAGE SECTION' in up
    # Um copybook (fragmento) normalmente comeca direto em nivel 01/05 ou REDEFINES,
    # sem IDENTIFICATION DIVISION / PROGRAM-ID.
    if tem_id_div or tem_proc_div:
        return 'PROGRAMA'
    # Se comeca com nivel de dado (01, 05, etc.) ou REDEFINES -> copybook
    primeiras = [l.strip() for l in txt.splitlines() if l.strip() and not l.strip().startswith('*')][:5]
    corpo = ' '.join(primeiras).upper()
    if re.search(r'\b01\b|\b05\b|REDEFINES|PICTURE|PIC ', corpo):
        return 'COPYBOOK'
    return 'INDEFINIDO'

with zipfile.ZipFile(z) as zf:
    nomes = sorted(n for n in zf.namelist()
                   if n.startswith('Convertidos/') and not n.endswith('/'))
    resultados = []
    for n in nomes:
        base = n.split('/')[-1]
        txt = zf.read(n).decode('latin-1', errors='ignore')
        tipo = classificar(base, txt)
        # Detectar se ha COPY dentro (programas costumam ter varios COPY)
        n_copy = len(re.findall(r'\bCOPY\s+[\w-]+', txt.upper()))
        # Primeira linha de dado significativa
        prog_id = ''
        m = re.search(r'PROGRAM-ID\.\s*([\w-]+)', txt.upper())
        if m:
            prog_id = m.group(1)
        resultados.append((base, tipo, n_copy, prog_id, len(txt.splitlines())))

print(f'{"ARQUIVO":<12} {"TIPO":<10} {"#COPY":>5} {"LINHAS":>7}  PROGRAM-ID')
print('-' * 60)
progs = 0
copys = 0
for base, tipo, n_copy, prog_id, nl in resultados:
    if tipo == 'PROGRAMA':
        progs += 1
    elif tipo == 'COPYBOOK':
        copys += 1
    print(f'{base:<12} {tipo:<10} {n_copy:>5} {nl:>7}  {prog_id}')

print('-' * 60)
print(f'Total: {len(resultados)} arquivos | PROGRAMAS: {progs} | COPYBOOKS: {copys}')
print()
print('COPYBOOKS encontrados:')
print('  ' + ', '.join(b for b, t, *_ in resultados if t == 'COPYBOOK'))
