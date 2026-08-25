import re
from pathlib import Path

BASE = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos')
# Todos os arquivos da entrega (Convertidos + Originais + a planilha ignoramos)
arquivos = [f for f in BASE.rglob('*') if f.is_file() and f.suffix.lower() not in ('.xlsx',)]

def ler(f):
    return f.read_text(encoding='latin-1', errors='ignore')

# Concatena TODO o conteudo da entrega
corpus = {}
for f in arquivos:
    corpus[f.relative_to(BASE).as_posix()] = ler(f)

# Lista de faltantes (do CSV gerado)
faltantes = []
csv = Path('docs/analise/COPYBOOKS_FALTANTES.csv').read_text(encoding='utf-8-sig').splitlines()[1:]
for linha in csv:
    faltantes.append(linha.split(';')[0].strip())

# Para cada faltante, verificar se seu NOME aparece como DEFINICAO
# (nao apenas como "COPY X", mas como label 01 X, ou nome de estrutura)
print('Verificando se algum copybook faltante esta DEFINIDO dentro de algum arquivo')
print('(procura o nome como nivel 01/05, ou fora de uma instrucao COPY)')
print('=' * 70)

achados = []
for cp in faltantes:
    # Procura o nome do copybook em qualquer arquivo, EXCETO precedido por "COPY "
    for rel, txt in corpus.items():
        for m in re.finditer(re.escape(cp), txt, re.IGNORECASE):
            ini = max(0, m.start() - 8)
            trecho_antes = txt[ini:m.start()].upper()
            if 'COPY' not in trecho_antes:
                # achou o nome fora de um COPY -> possivel definicao embutida
                achados.append((cp, rel, txt[max(0,m.start()-30):m.start()+40].replace(chr(10),' ')))
                break
        else:
            continue
        break

if achados:
    print(f'POSSIVEIS definicoes embutidas encontradas: {len(achados)}')
    for cp, rel, ctx in achados:
        print(f'  {cp} em {rel}: ...{ctx}...')
else:
    print('NENHUM copybook faltante aparece definido dentro de outro arquivo.')
    print('Todos so aparecem como instrucao "COPY <nome>." (chamada, nao definicao).')

print()
print('=' * 70)
# Verificacao complementar: os arquivos entregues contem SECTIONS de dados
# grandes que poderiam conter multiplos copybooks embutidos?
print('Tamanho dos 14 copybooks entregues (linhas) - para ver se algum e "grande"')
print('(um copybook consolidado teria centenas/milhares de linhas):')
conv = BASE / 'Convertidos'
for f in sorted(conv.iterdir()):
    if f.is_file():
        txt = ler(f).upper()
        if 'PROGRAM-ID' not in txt and 'IDENTIFICATION DIVISION' not in txt:
            print(f'  {f.name:<10} {len(ler(f).splitlines()):>5} linhas')
