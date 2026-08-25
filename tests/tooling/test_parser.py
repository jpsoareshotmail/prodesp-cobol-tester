"""Teste rapido do copybook_parser (roda da raiz do projeto: py tooling/_test_parser.py)."""
from tooling.copybook_parser import parse_copybook, parse_file, iter_elementary

print('=== Teste 1: COFI04 real (entrega) ===')
p = 'entregas/copybook-Amostragem POC  - Fontes Convertidos/Originais/MAPA_COFI04.cpy'
campos = parse_file(p)
elem = list(iter_elementary(campos))
print(f'Campos raiz: {len(campos)} | campos elementares (sem FILLER): {len(elem)}')
for trilha, c in elem[:8]:
    grp = '/'.join(t.name for t in trilha)
    print(f'  {grp} > {c.name:<14} {c.pic.category:<12} len={c.pic.length} nul={c.nullable}')

print('\n=== Teste 2: casos sinteticos (COMP-3, V decimal, OCCURS, S) ===')
sample = """
       01  REG-TESTE.
           05  T-CODIGO        PIC 9(009).
           05  T-VALOR         PIC S9(7)V99 COMP-3.
           05  T-SALDO         PIC 9(5)V9(3).
           05  T-NOME          PIC X(030).
           05  T-QTD           PIC 9(4) COMP.
           05  T-FLAG-NUL.
               07  T-FLAG      PIC 9(001).
           05  T-ITENS OCCURS 12 TIMES.
               07  T-ITEM      PIC X(005).
"""
campos = parse_copybook(sample)
for trilha, c in iter_elementary(campos):
    grp = '/'.join(t.name for t in trilha)
    p = c.pic
    print(f'  {grp} > {c.name:<10} cat={p.category:<12} int={p.integer_digits} dec={p.decimal_digits} '
          f'sign={p.signed} usage={p.usage:<7} nul={c.nullable}')
# validar OCCURS detectado no grupo
def find(nodes, nome):
    for n in nodes:
        if n.name == nome:
            return n
        r = find(n.children, nome)
        if r:
            return r
itens = find(campos, 'T-ITENS')
print(f'\n  T-ITENS OCCURS = {itens.occurs} (esperado 12)')
