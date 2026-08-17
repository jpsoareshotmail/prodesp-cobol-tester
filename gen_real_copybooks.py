"""
Generate complete copybooks (WSD*, PDD*) from FETCH INTO host variables.
These copybooks define the record areas that the converted programs expect.
The source code is NOT modified - only copybooks are generated.
"""
import re
from pathlib import Path

CONV_DIR = Path('fontes_convertidos/Convertidos')
COPY_DIR = Path('cobol_build/copy')
PREFIX = '       '  # 7 spaces (col 1-6 seq + col 7 space)
INDENT = '           '  # 11 spaces (Area B)

# Extract all host variables from FETCH INTO across all programs
def extract_all_host_vars():
    """Extract host vars and their dataset groupings from all programs."""
    all_vars = {}  # {prefix: {varname: set(programs)}}
    
    for f in sorted(CONV_DIR.iterdir()):
        if not f.is_file() or f.name.startswith('MAPA'):
            continue
        content = f.read_text(encoding='latin-1')
        
        # Extract from FETCH INTO
        fetches = re.findall(r'FETCH\s+[\w-]+\s+INTO\s+(.*?)(?:END-EXEC|$)', content, re.DOTALL)
        for fetch in fetches:
            vars_in_fetch = re.findall(r':([A-Za-z][\w-]*)', fetch)
            for v in vars_in_fetch:
                parts = v.split('-')
                if len(parts) >= 2:
                    prefix = parts[0]
                    if prefix not in all_vars:
                        all_vars[prefix] = {}
                    all_vars[prefix][v] = all_vars[prefix].get(v, set())
                    all_vars[prefix][v].add(f.name)
        
        # Also extract from MOVE statements involving host vars
        # Pattern: MOVE :VAR TO something or MOVE something TO :VAR
        moves = re.findall(r':([A-Za-z][\w-]*)', content)
        for v in moves:
            parts = v.split('-')
            if len(parts) >= 2:
                prefix = parts[0]
                if prefix not in all_vars:
                    all_vars[prefix] = {}
                if v not in all_vars[prefix]:
                    all_vars[prefix][v] = set()
                all_vars[prefix][v].add(f.name)
    
    return all_vars


def infer_pic(varname):
    """Infer PIC clause from variable name patterns."""
    upper = varname.upper()
    
    # ROWID fields
    if 'ROWID' in upper:
        return 'PIC X(018)'
    
    # Remove -X suffix for analysis
    base = upper.rstrip('-X') if upper.endswith('-X') else upper
    
    # Date fields
    if any(x in base for x in ['-DT-', '-DATA', '-DATE', 'DT-INCL', 'DT-EXCL',
            'DT-INCLUSAO', 'DT-EXCLUSAO', 'DT-VALID', 'DT-NASC', 'DT-OBITO',
            'DT-PROT', 'DT-CADAST', 'DT-EMIS', 'DT-PAG', 'DT-ATRIB',
            'DT-ENVIO', 'DT-ATUAL', 'DT-HIST', 'DT-OCORR', 'DT-VENDA',
            'DT-DOCTS', 'DT-NFISCAL', 'DT-GRAV', 'DT-INC', 'DT-REC']):
        return 'PIC X(010)'
    
    # Time fields
    if any(x in base for x in ['-HR-', '-HORA', 'HR-INCL', 'HR-EXCL',
            'HR-INCLUSAO', 'HR-EXCLUSAO', 'HR-ENVIO', 'HR-GRAV']):
        return 'PIC X(006)'
    
    # Year fields
    if any(x in base for x in ['-ANO-', '-ANO', 'ANOFABR', 'ANOMOD', 'ANO-X']):
        return 'PIC X(004)'
    
    # CPF/CNPJ
    if 'CPF' in base and 'CGC' in base:
        return 'PIC X(014)'
    if 'CPF' in base:
        return 'PIC X(011)'
    if 'CNPJ' in base or 'CGC' in base:
        return 'PIC X(014)'
    
    # Placa
    if 'PLACA' in base:
        return 'PIC X(010)'
    
    # Chassi
    if 'CHASSI' in base or 'CHASSIS' in base:
        return 'PIC X(021)'
    
    # UF
    if base.endswith('-UF') or '-UF-' in base or 'SIG-EST' in base:
        return 'PIC X(002)'
    
    # Municipio code
    if 'MUNICIPIO' in base or 'MUNIC' in base or 'MUN-' in base:
        return 'PIC X(005)'
    
    # CEP
    if 'CEP' in base:
        return 'PIC X(008)'
    
    # Phone
    if 'TELEFONE' in base or 'RAMAL' in base or 'DDD' in base:
        return 'PIC X(010)'
    
    # Names (longer fields)
    if any(x in base for x in ['NOME', 'ENDERECO', 'LOGRADOURO', 'BAIRRO',
            'CIDADE', 'COMPL', 'OBSERV', 'INFORMACOES', 'DESCR']):
        return 'PIC X(040)'
    
    # Codes
    if any(x in base for x in ['-COD-', 'CODIGO', '-CD-', '-TIP-', 'TIPO',
            'CATEG', 'MARCA', 'COR-', 'COMBUS', 'ESPECIE']):
        return 'PIC X(006)'
    
    # Renavam
    if 'RENAVAM' in base:
        return 'PIC X(011)'
    
    # Numbers/sequences
    if any(x in base for x in ['-NUM-', '-NR-', '-SEQ-', '-QTD-', 'CONTRATO',
            'PROCESSO', 'PROTOC', 'OFIC']):
        return 'PIC X(010)'
    
    # Binary/status fields
    if any(x in base for x in ['FILLER', 'BIN-', 'SITUACAO', 'STATUS']):
        return 'PIC X(020)'
    
    # BO (Boletim Ocorrencia)
    if 'BO-' in base or 'BOSPJ' in base:
        return 'PIC X(012)'
    
    # User fields
    if 'USU-' in base or 'USUARIO' in base or 'USER' in base:
        return 'PIC X(008)'
    
    # Default
    return 'PIC X(030)'


def get_dataset_name(prefix):
    """Map prefix to dataset name (01 level group)."""
    # Dataset names found in programs
    known = {
        'ALE': 'ALERTADS', 'QXA': 'QUEIXADS', 'REC': 'RECUPERADODS',
        'BR': 'TABMUNBRDS', 'BLO': 'BLOQUEIODS', 'DES': 'DESBLOQUEIODS',
        'TAB': 'DETTABDS', 'CVV': 'COMVENDS', 'CVH': 'COMVENDHISDS',
        'GER': 'GEVERDS', 'GEX': 'GEVEXCLUIDODS', 'GVM': 'GEVMODIFDS',
        'GRA': 'GRAVAMESDS', 'GRC': 'GRAVAMECONTRDS', 'INS': 'INSPECAODS',
        'LAC': 'LACRACAODS', 'MOD': 'MODIFICADODS', 'NPL': 'NOVAPLACDS',
        'OBS': 'OBSERVCRLVDS', 'SEG': 'SEGURADORADS', 'TAX': 'TAXADS',
        'USU': 'USUARIODS', 'VAL': 'VALIDACAODS', 'VIS': 'VISTORIADS',
        'EAU': 'ECRVAUTENTICADS', 'ESP': 'ESPELHODS', 'ETP': 'ESTAMPAGEMDS',
        'PLC': 'PRODPLCDS', 'PLI': 'PRODPLIDS', 'CRT': 'PRODCRTDS',
        'CRV': 'PRODCRVDS', 'DUT': 'PRODDUTDS', 'ARR': 'PRODARRDS',
        'PRT': 'PROTGEVDS', 'SIR': 'SIRCOFDS', 'RNV': 'RENAVEDS',
        'RNH': 'RENAVEHISDS', 'CAM': 'CAMBIODS', 'MTR': 'MOTORDS',
        'BLD': 'BLINDADOSDS', 'AVA': 'AVARIADOSDS', 'AVH': 'AVARIAHISTDS',
        'CSV': 'CSVCERTDS', 'REJ': 'RENAJUDDS', 'EPC': 'ESCPLACDS',
        'DSP': 'DESPACHANTEDS', 'FCG': 'CNPJOFICIALDS', 'NTF': 'NTFISCALDS',
        'OBI': 'BLOQOBITODS', 'SLV': 'EMPSALVADOSDS', 'TAV': 'TAXASDS',
        'PPV': 'PROPRIETPROVDS', 'GEI': 'GEVINATIVODS', 'GEL': 'GEVLACRACAODS',
        'CIP': 'VEICCODIPVADS', 'AST': 'IPVAASTDS', 'AUT': 'AUTENTICACAODS',
        'CSC': 'CODSEGCRVDS', 'CSL': 'CODSEGCRLVDS', 'PCM': 'PRECADCICLODS',
        'PLA': 'PRODPLACDS', 'LIV': 'VALIDADOSDS', 'ORG': 'FINCONGRADS',
        'CHA': 'PRODCHASSIDS', 'PROT': 'PRODPROTDS',
    }
    return known.get(prefix, f'{prefix}DS')


def generate_wsd_copybook(prefix, fields):
    """Generate a WSD copybook for a dataset prefix."""
    ds_name = get_dataset_name(prefix)
    lines = []
    lines.append(f'{PREFIX[:-1]}* WSD copybook for {ds_name} (auto-generated)')
    lines.append(f'{PREFIX}01  {ds_name}.')
    
    # Add ROWID first if exists
    rowid_var = f'{ds_name}-ROWID'
    lines.append(f'{INDENT}05  {rowid_var:<30} PIC X(018).')
    
    # Add all fields
    for field in sorted(fields):
        pic = infer_pic(field)
        lines.append(f'{INDENT}05  {field:<30} {pic}.')
    
    # Also add non-X versions for numeric fields used in comparisons
    for field in sorted(fields):
        if field.endswith('-X'):
            base = field[:-2]
            pic_base = infer_pic(base)
            # Numeric version
            if any(x in base.upper() for x in ['-DT-', '-HR-', '-ANO', 'MUNICIPIO',
                    '-COD-', '-NUM-', '-SEQ-', '-QTD-']):
                lines.append(f'{INDENT}05  {base:<30} PIC 9(009).')
            else:
                lines.append(f'{INDENT}05  {base:<30} {pic_base}.')
    
    return '\n'.join(lines) + '\n'


def generate_pdd_copybook(prefix):
    """Generate a PDD copybook (procedure division paragraphs for DB access)."""
    ds_name = get_dataset_name(prefix)
    lines = []
    lines.append(f'{PREFIX[:-1]}* PDD copybook for {ds_name} (auto-generated)')
    lines.append(f'{PREFIX}{ds_name}-DB2DMS.')
    lines.append(f'{INDENT}CONTINUE.')
    return '\n'.join(lines) + '\n'


def main():
    print('Extracting host variables from all programs...')
    all_vars = extract_all_host_vars()
    print(f'Found {sum(len(v) for v in all_vars.values())} variables in {len(all_vars)} datasets')
    
    # Determine which copybooks map to which datasets
    # WSD01118 -> most used, likely the main vehicle record (GER/PLC/PLI)
    # Need to map copybook names to dataset prefixes
    
    # For now, generate one master copybook per dataset that defines ALL fields
    # The existing WSD* stubs will be replaced with real definitions
    
    generated = 0
    for prefix, fields in sorted(all_vars.items()):
        if len(fields) < 2:  # Skip single-field datasets (just ROWID)
            continue
        
        # Skip FILLER prefixes
        if prefix.startswith('FILLER'):
            continue
            
        ds_name = get_dataset_name(prefix)
        
        # Generate WSD-style copybook
        wsd_name = f'WSD-{ds_name}.cpy'
        wsd_path = COPY_DIR / wsd_name
        content = generate_wsd_copybook(prefix, fields)
        wsd_path.write_text(content, encoding='latin-1')
        generated += 1
    
    # Now update the existing stub copybooks to include the real definitions
    # The WSGL copybook should include all dataset definitions
    # Strategy: create a master WSGL-DATASETS.cpy that WSGL includes
    
    master_ws = []
    master_ws.append(f'{PREFIX[:-1]}* Master dataset definitions (auto-generated)')
    
    for prefix, fields in sorted(all_vars.items()):
        if len(fields) < 2 or prefix.startswith('FILLER'):
            continue
        ds_name = get_dataset_name(prefix)
        master_ws.append(f'{PREFIX}01  {ds_name}.')
        rowid_var = f'{ds_name}-ROWID'
        master_ws.append(f'{INDENT}05  {rowid_var:<30} PIC X(018).')
        for field in sorted(fields):
            pic = infer_pic(field)
            master_ws.append(f'{INDENT}05  {field:<30} {pic}.')
        # Non-X versions
        for field in sorted(fields):
            if field.endswith('-X'):
                base = field[:-2]
                if any(x in base.upper() for x in ['-DT-', '-HR-', '-ANO', 'MUNICIPIO',
                        '-COD-', '-NUM-', '-SEQ-', '-QTD-']):
                    master_ws.append(f'{INDENT}05  {base:<30} PIC 9(009).')
                else:
                    pic_base = infer_pic(base)
                    master_ws.append(f'{INDENT}05  {base:<30} {pic_base}.')
        master_ws.append('')
    
    # Write master datasets file
    master_path = COPY_DIR / 'WSGL-DATASETS.cpy'
    master_path.write_text('\n'.join(master_ws), encoding='latin-1')
    
    # Update WSGLDB to include the master datasets
    wsgldb_path = COPY_DIR / 'WSGLDB.cpy'
    wsgldb_content = wsgldb_path.read_text(encoding='latin-1')
    if 'COPY WSGL-DATASETS' not in wsgldb_content:
        wsgldb_content += f'\n{PREFIX}COPY WSGL-DATASETS.\n'
        wsgldb_path.write_text(wsgldb_content, encoding='latin-1')
    
    print(f'Generated {generated} WSD copybooks + master WSGL-DATASETS.cpy')
    print(f'Total fields defined: {sum(len(v) for v in all_vars.values() if len(v) >= 2)}')


if __name__ == '__main__':
    main()
