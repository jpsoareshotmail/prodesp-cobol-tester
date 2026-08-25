import sys
sys.path.insert(0, 'app')
from cobol_runner import compilar_modulo
from pathlib import Path

SKIP = {'AUML01','CAPA01','CCCC99','COFI02','COFI04','COFI11',
        'EMIS98','EMIS99','EMPA01','GERA01','MENS01','MENS03','RENA01','RENA04'}

progs = [f.name for f in sorted(Path('fontes_convertidos/Convertidos').iterdir())
         if f.is_file() and not f.name.startswith('MAPA') and f.name not in SKIP]

ok = 0
fail = 0
fails = []
for p in progs:
    r = compilar_modulo(p)
    if r[0]:
        ok += 1
    else:
        fail += 1
        fails.append(p)
        print(f'  FAIL {p}')

print(f'\n=== OK={ok} FAIL={fail} Total={ok+fail} ===')
if fails:
    print('Falhas:', ', '.join(fails))
