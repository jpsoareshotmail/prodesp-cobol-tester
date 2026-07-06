"""
Pre-processador EXEC SQL para GnuCOBOL.

Remove/comenta blocos EXEC SQL ... END-EXEC dos fontes convertidos,
permitindo compilacao sem pre-processador Oracle/DB2.

Estrategia:
- EXEC SQL DECLARE ... END-EXEC -> comentado (declaracoes de cursor)
- EXEC SQL INCLUDE ... END-EXEC -> comentado (includes de SQL)
- EXEC SQL OPEN/CLOSE/FETCH ... END-EXEC -> substituido por CONTINUE
- EXEC SQL SELECT/INSERT/UPDATE/DELETE ... END-EXEC -> substituido por
  MOVE "00" TO WS-DB-STATUS (simula sucesso)
- EXEC SQL WHENEVER ... END-EXEC -> comentado
"""

import re
from pathlib import Path


def preprocessar_sql(source_content: str) -> str:
    """
    Remove blocos EXEC SQL/CICS do fonte COBOL, substituindo por stubs.
    Preserva nomes de paragrafos que precedem EXEC SQL.
    Blocos antes da PROCEDURE DIVISION sao apenas comentados.
    Blocos na PROCEDURE DIVISION recebem CONTINUE.
    """
    lines = source_content.split('\n')
    result = []
    in_exec_sql = False
    exec_sql_lines = []
    in_procedure_div = False

    i = 0
    while i < len(lines):
        line = lines[i]
        upper_stripped = line.strip().upper()

        # Detectar PROCEDURE DIVISION
        if 'PROCEDURE' in upper_stripped and 'DIVISION' in upper_stripped and not upper_stripped.startswith('*'):
            in_procedure_div = True

        # Detectar inicio de bloco EXEC SQL ou EXEC CICS
        if ('EXEC SQL' in line.upper() or 'EXEC CICS' in line.upper()) and not in_exec_sql:
            if 'END-EXEC' in line.upper():
                result.append(_comment_line(line))
                if in_procedure_div:
                    # Checar se termina com ponto (area B, colunas 8-72)
                    code_area = line[6:72] if len(line) > 72 else line[6:]
                    if '.' in code_area and code_area.strip().rstrip().endswith('.'):
                        result.append('           CONTINUE.')
                    elif 'END-EXEC.' in line.upper():
                        result.append('           CONTINUE.')
                    else:
                        result.append('           CONTINUE')
                i += 1
                continue
            in_exec_sql = True
            exec_sql_lines = [line]
            i += 1
            continue

        # Dentro de bloco EXEC SQL
        if in_exec_sql:
            exec_sql_lines.append(line)
            if 'END-EXEC' in line.upper():
                in_exec_sql = False
                # Comentar tudo
                for el in exec_sql_lines:
                    result.append(_comment_line(el))
                if in_procedure_div:
                    # Se a ultima linha do bloco terminava com ponto, adicionar ponto
                    last_line = exec_sql_lines[-1]
                    code_area = last_line[6:72] if len(last_line) > 72 else last_line[6:]
                    if 'END-EXEC.' in last_line.upper() or code_area.rstrip().endswith('.'):
                        result.append('           CONTINUE.')
                    else:
                        result.append('           CONTINUE')
                exec_sql_lines = []
            i += 1
            continue

        # Linha normal na PROCEDURE DIVISION
        if in_procedure_div:
            # Comentar PERFORMs e CALLs de paragrafos de DB (Micro Focus syntax)
            if 'PERFORM' in line.upper() or 'CALL' in line.upper():
                upper_line = line.upper().strip()
                if any(x in upper_line for x in ['DATABASE-OPEN', 'DATABASE-CLOSE',
                        'DATABASE-TERMINATE', 'HANDLE-DMTERMINATE', 'HANDLE-SQL',
                        'SYSTEM  DMTERMINATE', 'SYSTEM DMTERMINATE',
                        '-STEN', ':TRUE)']):
                    result.append(_comment_line(line))
                    if line.strip().endswith('.') or 'END-EXEC.' in line.upper():
                        code_area = line[6:72] if len(line) > 72 else line[6:]
                        if code_area.rstrip().endswith('.'):
                            result.append('           CONTINUE.')
                        else:
                            result.append('           CONTINUE')
                    else:
                        result.append('           CONTINUE')
                    i += 1
                    continue

            # Detectar paragrafo cujo corpo e' inteiramente EXEC SQL
            # Padrao: nome de paragrafo seguido de EXEC SQL na proxima linha nao-vazia
            if _is_paragraph_name(line):
                # Verificar se as proximas linhas sao EXEC SQL
                next_exec = _find_next_exec(lines, i + 1)
                if next_exec is not None:
                    # Manter o nome do paragrafo, comentar o EXEC SQL
                    result.append(line)  # preserva nome do paragrafo
                    i += 1
                    continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def _is_paragraph_name(line: str) -> bool:
    """Verifica se a linha e' um nome de paragrafo COBOL (Area A, termina com .)"""
    if len(line) < 8:
        return False
    if line[6] == '*':  # comentario
        return False
    # Paragrafo: comeca na coluna 8 (Area A), contem nome seguido de .
    stripped = line[7:].strip()
    if not stripped:
        return False
    # Deve ser um identificador seguido de ponto
    if re.match(r'^[\w-]+\.\s*$', stripped):
        return True
    return False


def _find_next_exec(lines: list, start: int) -> int:
    """Procura EXEC SQL/CICS nas proximas linhas (pulando vazias e comentarios)."""
    for j in range(start, min(start + 5, len(lines))):
        stripped = lines[j].strip()
        if not stripped:
            continue
        if len(lines[j]) >= 7 and lines[j][6] == '*':
            continue
        if 'EXEC SQL' in lines[j].upper() or 'EXEC CICS' in lines[j].upper():
            return j
        return None  # primeira linha nao-vazia nao e' EXEC
    return None

    return '\n'.join(result)


def _comment_line(line: str) -> str:
    """Comenta uma linha COBOL mantendo o formato fixo."""
    if len(line) >= 7:
        return line[:6] + '*' + line[7:]
    elif line.strip():
        return '      * ' + line.strip()
    return line


def preprocessar_arquivo(source_path: Path, output_path: Path) -> tuple:
    """
    Pre-processa um arquivo COBOL removendo EXEC SQL e gerando
    definicoes para host variables.
    Retorna (sucesso, mensagem).
    """
    try:
        content = source_path.read_text(encoding='latin-1')

        if 'EXEC SQL' not in content.upper() and 'EXEC CICS' not in content.upper():
            # Nao tem SQL, copiar direto
            output_path.write_text(content, encoding='latin-1')
            return True, "Sem SQL (copiado direto)"

        # Extrair host variables (precedidas por : em SQL)
        host_vars = set(re.findall(r':([A-Za-z][\w-]*)', content))

        # Processar SQL
        processed = preprocessar_sql(content)

        # Adicionar COPY de table stubs se necessario (para programas com EXEC SQL)
        # Inserir antes da LINKAGE SECTION
        table_copy = f'       COPY {source_path.stem}-TABLES.\n'
        table_cpy = Path(output_path).parent / 'copy' / f'{source_path.stem}-TABLES.cpy'
        if table_cpy.exists():
            for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
                if marker in processed:
                    processed = processed.replace(marker, table_copy + marker, 1)
                    break
            # Nao gerar host vars se tables.cpy existe (evita duplicacao)
            host_vars = set()

        # Adicionar declaracoes de host variables no WORKING-STORAGE
        if host_vars:
            var_decls = _gerar_host_vars(host_vars, content)
            # Inserir antes da LINKAGE SECTION ou PROCEDURE DIVISION
            inserted = False
            for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
                if marker in processed:
                    processed = processed.replace(
                        marker,
                        var_decls + '\n' + marker,
                        1
                    )
                    inserted = True
                    break
            if not inserted:
                # Fallback: inserir antes da ultima linha do WORKING-STORAGE
                for marker in ['LINKAGE SECTION', 'PROCEDURE   DIVISION', 'PROCEDURE DIVISION']:
                    if marker in processed:
                        processed = processed.replace(marker, var_decls + '\n       ' + marker, 1)
                        break

        output_path.write_text(processed, encoding='latin-1')

        original_count = content.upper().count('EXEC SQL')
        return True, f"Processado ({original_count} blocos SQL, {len(host_vars)} host vars)"

    except Exception as e:
        return False, str(e)


def _gerar_host_vars(host_vars: set, content: str) -> str:
    """Gera declaracoes COBOL para host variables extraidas do SQL."""
    lines = []
    lines.append('      * Host variables (gerado automaticamente)')

    # Tambem capturar nomes de datasets referenciados (xxxDS patterns)
    ds_names = set(re.findall(r'\b(\w+DS)\b', content))
    all_needed = host_vars | ds_names

    for var in sorted(all_needed):
        # Pular se ja esta definido no fonte (busca simples)
        var_pattern = f' {var} '
        var_pattern2 = f' {var}.'
        if var_pattern in content or var_pattern2 in content:
            continue

        # Inferir tipo pelo nome
        if any(x in var.upper() for x in ['PLACA', 'NOME', 'DESC', 'END', 'TIPO',
                'STATUS', 'UF', 'MARCA', 'MODELO', 'COR', 'CHASSI', 'RENAVAM',
                'CPF', 'CNPJ', 'RG', 'DELEG', 'MUNIC']):
            pic = 'PIC X(050) VALUE SPACES.'
        elif any(x in var.upper() for x in ['DATA', 'DT-', 'DATE', 'HR-']):
            pic = 'PIC X(010) VALUE SPACES.'
        elif any(x in var.upper() for x in ['COD', 'NUM', 'SEQ', 'QTD', 'ANO']):
            pic = 'PIC 9(009) VALUE ZEROS.'
        elif any(x in var.upper() for x in ['VALOR', 'VLR', 'PRECO']):
            pic = 'PIC 9(013)V99 VALUE ZEROS.'
        elif 'ROWID' in var.upper():
            pic = 'PIC X(018) VALUE SPACES.'
        elif var.upper().endswith('DS'):
            # Dataset name - group item
            pic = 'PIC X(001) VALUE SPACES.'
        else:
            pic = 'PIC X(050) VALUE SPACES.'

        # Gerar nome valido COBOL (max 30 chars)
        var_name = var[:30]
        lines.append(f'       01  {var_name:<30} {pic}')

    return '\n'.join(lines) + '\n'
