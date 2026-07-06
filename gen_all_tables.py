"""
Gera copybooks -TABLES.cpy automaticamente para todos os programas
convertidos que usam EXEC SQL, extraindo os campos de tabela do fonte.
"""
import re
from pathlib import Path

CONV_DIR = Path('fontes_convertidos/Convertidos')
COPY_DIR = Path('cobol_build/copy')


def extrair_campos_tabela(content: str) -> dict:
    """Extrai campos de tabelas (prefixos de 2-4 letras) usados no programa."""
    # Encontrar todos os identificadores com padrao PREFIX-CAMPO
    all_ids = re.findall(r'\b([A-Z]{2,4})-([A-Z][\w-]*)\b', content)
    
    # Agrupar por prefixo
    tabelas = {}
    for prefix, campo in all_ids:
        # Ignorar prefixos comuns que nao sao tabelas
        if prefix in ('WS', 'LC', 'AX', 'SC', 'IF', 'GO', 'TO', 'OR', 'LS',
                      'PC', 'PF', 'SP', 'DB', 'DM', 'MN', 'CT'):
            continue
        full_name = f'{prefix}-{campo}'
        if prefix not in tabelas:
            tabelas[prefix] = set()
        tabelas[prefix].add(full_name)
    
    return tabelas


def inferir_pic(campo: str) -> str:
    """Infere o PIC baseado no nome do campo."""
    upper = campo.upper()
    if any(x in upper for x in ['-DT-', 'DATA', 'DATE']):
        return 'PIC 9(008) VALUE ZEROS.'
    elif any(x in upper for x in ['-HR-', 'HORA', 'TIME']):
        return 'PIC 9(006) VALUE ZEROS.'
    elif any(x in upper for x in ['-COD-', '-NUM-', '-SEQ-', 'MUNICIPIO', '-ANO']):
        return 'PIC 9(009) VALUE ZEROS.'
    elif 'ROWID' in upper:
        return 'PIC X(018) VALUE SPACES.'
    elif upper.endswith('-X'):
        # Campo alfanumerico (sufixo -X indica host var string)
        base = upper[:-2]
        if 'PLACA' in base:
            return 'PIC X(010) VALUE SPACES.'
        elif 'UF' in base:
            return 'PIC X(002) VALUE SPACES.'
        elif 'CHASSIS' in base:
            return 'PIC X(021) VALUE SPACES.'
        elif 'NOME' in base or 'LOGRA' in base:
            return 'PIC X(040) VALUE SPACES.'
        elif 'CEP' in base:
            return 'PIC X(008) VALUE SPACES.'
        elif 'SIG' in base:
            return 'PIC X(002) VALUE SPACES.'
        elif 'LIT' in base:
            return 'PIC X(040) VALUE SPACES.'
        elif 'FILLER' in base:
            return 'PIC X(020) VALUE SPACES.'
        else:
            return 'PIC X(030) VALUE SPACES.'
    else:
        return 'PIC X(030) VALUE SPACES.'


def gerar_tables_cpy(prog_name: str, content: str) -> str:
    """Gera o conteudo do copybook -TABLES.cpy para um programa."""
    tabelas = extrair_campos_tabela(content)
    
    if not tabelas:
        return ''
    
    # Encontrar nomes de datasets (xxxDS) usados no programa
    ds_names = set(re.findall(r'\b(\w+DS)\b', content))
    
    # Encontrar variaveis ja definidas no fonte (fora de EXEC SQL e comentarios)
    lines = content.split('\n')
    defined_vars = set()
    in_exec = False
    for line in lines:
        if 'EXEC SQL' in line.upper():
            in_exec = True
        if in_exec:
            if 'END-EXEC' in line.upper():
                in_exec = False
            continue
        if len(line) >= 7 and line[6] == '*':
            continue
        # Extrair nomes de variaveis definidas (01/05/10/15/20 NOME PIC...)
        m = re.match(r'\s+\d{2}\s+([A-Z][\w-]+)', line.strip())
        if m:
            defined_vars.add(m.group(1))
    
    lines_out = []
    lines_out.append(f'      * Record areas para {prog_name} (gerado automaticamente)')
    
    for ds in sorted(ds_names):
        prefix = None
        if ds == 'ALERTADS': prefix = 'ALE'
        elif ds == 'QUEIXADS': prefix = 'QXA'
        elif ds == 'RECUPERADODS': prefix = 'REC'
        elif ds == 'TABMUNBRDS': prefix = 'BR'
        elif ds.endswith('DS'):
            base = ds[:-2]
            for p in tabelas:
                if base.startswith(p) or p.startswith(base[:3]):
                    prefix = p
                    break
        
        if prefix and prefix in tabelas:
            # Verificar se o dataset ja esta definido
            if ds in defined_vars:
                continue
            lines_out.append(f'       01  {ds}.')
            for campo in sorted(tabelas[prefix]):
                # Pular se ja esta definido no fonte
                if campo in defined_vars:
                    continue
                pic = inferir_pic(campo)
                lines_out.append(f'           05  {campo:<30} {pic}')
            lines_out.append('')
    
    return '\n'.join(lines_out) + '\n'


def main():
    count = 0
    for f in sorted(CONV_DIR.iterdir()):
        if not f.is_file():
            continue
        content = f.read_text(encoding='latin-1')
        if 'EXEC SQL' not in content:
            continue
        
        cpy_name = f'{f.name}-TABLES.cpy'
        cpy_path = COPY_DIR / cpy_name
        
        # Pular se ja existe (ex: FGAA012D-TABLES.cpy feito manualmente)
        if cpy_path.exists():
            print(f'  SKIP {f.name} (ja existe)')
            continue
        
        cpy_content = gerar_tables_cpy(f.name, content)
        if cpy_content.strip():
            cpy_path.write_text(cpy_content, encoding='latin-1')
            print(f'  OK   {f.name} -> {cpy_name}')
            count += 1
        else:
            print(f'  SKIP {f.name} (sem tabelas)')
    
    print(f'\nGerados {count} copybooks -TABLES.cpy')


if __name__ == '__main__':
    main()
