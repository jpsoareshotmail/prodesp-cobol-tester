"""Regenerate PDGLDB.cpy with proper COBOL fixed format."""
import re
from pathlib import Path

conv = Path('fontes_convertidos/Convertidos')
paras = set()
for f in conv.iterdir():
    if f.is_file():
        content = f.read_text(encoding='latin-1')
        paras.update(re.findall(r'\b(\w+-DB2DMS)\b', content))
        paras.update(re.findall(r'\b(9999-\w+)\b', content))

paras.add('HANDLE-SQL-ERRORS')
paras.add('HANDLE-DMTERMINATE')
paras.add('DATABASE-TERMINATE')
paras.add('9999-ABEND-TRAP')
paras.add('BLOCHASSE-STEN')
paras.add('BLOPLAMSE1-STBG')
paras.add('BLOPLAMSE2-STBG')
paras.add('CONTAINER-GET')
paras.add('CONTAINER-PUT')
paras.add('CONTAINER-RETURN')
paras.add('END-CONTAINER-GET')
paras.add('END-CONTAINER-PUT')
paras.add('END-CONTAINER-RETURN')

# Filter out -FL names (these are variables/flags, not paragraphs)
paras = {p for p in paras if not p.endswith('-FL')}

# 7 spaces = columns 1-6 (sequence) + column 7 (indicator=space)
# Paragraph name starts at column 8 (Area A)
PREFIX = '       '  # 7 spaces
INDENT = '           '  # 11 spaces (Area B)

with open('cobol_build/copy/PDGLDB.cpy', 'w', encoding='latin-1') as f:
    f.write(PREFIX[:-1] + '* PDGLDB - Generated DB paragraphs\n')
    for p in sorted(paras):
        f.write(PREFIX + p + '.\n')
        f.write(INDENT + 'CONTINUE.\n')

print(f'Generated PDGLDB.cpy with {len(paras)} paragraphs')

# Verify
with open('cobol_build/copy/PDGLDB.cpy', 'r') as f:
    line = f.readlines()[1]
    print(f'Line 2: len={len(line)} content={repr(line[:25])}')
