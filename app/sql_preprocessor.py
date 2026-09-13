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


def _reparar_literais_partidos(content: str) -> str:
    """Reparos de conversao seguros aplicados antes de compilar.

    (1) Neutraliza clausulas 'REDEFINES C-MAPA' orfas (mapas de tela cujo item
        base vem de um stub e nao precede imediatamente o REDEFINES), removendo
        o REDEFINES para permitir a compilacao. O overlay de memoria e perdido,
        o que e aceitavel para o teste isolado.

    (2) Neutraliza a continuacao orfa de 'INVOKE <dataset> USING ...' do DMS:
        o conversor comenta a linha do INVOKE e a linha do '01 X = Y' seguinte,
        mas deixa a linha 'USING ... .' descomentada, causando erro de sintaxe
        (verbo INVOKE removido, clausula USING sem statement). Comenta essa
        linha orfa tambem.

    (3) 'SELECT X ASSIGN TO X' (mesmo nome do arquivo e do assign, sem aspas):
        o GnuCOBOL tenta criar um item interno de assign dinamico com o mesmo
        nome do FD e da erro de redefinicao. Coloca o alvo do ASSIGN entre
        aspas (torna-o um literal, nao mais uma referencia a outro data-name).

    (4) 'PERFORM X OF Y-STBG' orfao: residuo de navegacao DMS (provavelmente
        um FIND/STORE do sub-schema original) que o conversor transformou num
        PERFORM sem paragrafo valido correspondente. Comenta a linha (nao ha
        equivalente sem runtime DMS real).

    (5) 'SET X OF Y' / 'TO BEGINNING' (2 linhas): posicionamento de cursor DMS
        ("ir para o primeiro registro do conjunto"), sem equivalente em COBOL
        padrao (SET so aceita INDEX/POINTER/numerico/condition-name). O
        conversor ja comenta a maioria das ocorrencias; as que sobraram sem
        comentar geram erro de sintaxe. Comenta as duas linhas.

    (6) Literal truncado 'DEAD*GOX*': defeito de transcricao no fonte original
        (nao e algo que o nosso pre-processador causa) - o conversor cortou
        'DEADLOCK' no meio e colou a tag de identificacao *GOX* logo depois,
        sem fechar a aspa. A mesma comparacao aparece correta ('DEADLOCK')
        em outro ponto do mesmo arquivo, confirmando o valor certo. Isso e
        reparado aqui (nao editando o fonte do usuario) para sobreviver a
        reimportacoes do arquivo original ainda corrompido.
    """
    # usado pelo reparo (3): se o fonte usa INVALID KEY em algum WRITE/READ,
    # um SELECT sem ORGANIZATION (default sequencial) nao aceita a clausula -
    # RELATIVE aceita INVALID KEY em acesso sequencial sem exigir uma chave
    # real (que nao temos, por ser campo do copybook original).
    usa_invalid_key = 'INVALID KEY' in content.upper()

    linhas = content.split('\n')
    saida = []
    pendente_invoke = False
    i = 0
    n = len(linhas)
    while i < n:
        ln = linhas[i]

        # ignora linhas de comentario (col 7 = '*' ou '/')
        if len(ln) >= 7 and ln[6] in ('*', '/'):
            if 'INVOKE' in ln.upper():
                pendente_invoke = True
            saida.append(ln)
            i += 1
            continue

        if not ln.strip():
            saida.append(ln)
            i += 1
            continue

        # (2) continuacao orfa de INVOKE comentado: proxima linha ativa e
        #     inteiramente "USING <campo(s)> ." -> e a continuacao perdida.
        if pendente_invoke:
            pendente_invoke = False
            musing = re.match(r'^\s{7,}USING\s+[A-Za-z0-9,\-\s]+\.\s*$', ln)
            if musing:
                saida.append(_comment_line(ln))
                i += 1
                continue

        # (5) 'SET X OF Y' seguido de 'TO BEGINNING' na proxima linha ativa
        mset = re.match(r'^\s*SET\s+[A-Za-z][\w-]*\s+OF\s+[A-Za-z][\w-]*\s*$', ln, re.IGNORECASE)
        if mset and i + 1 < n:
            prox = linhas[i + 1]
            if re.match(r'^\s*TO\s+BEGINNING\b', prox, re.IGNORECASE):
                saida.append(_comment_line(ln))
                saida.append(_comment_line(prox))
                i += 2
                continue

        # (1) REDEFINES orfao de mapa de tela: "01 X REDEFINES C-MAPA" quando
        #     C-MAPA vem de um stub e nao e o item imediatamente anterior.
        #     Remove a clausula REDEFINES para permitir compilar (overlay perdido,
        #     aceitavel para teste isolado).
        mred = re.match(r'^(\s*\d{2}\s+[A-Za-z][A-Za-z0-9\-]*)\s+REDEFINES\s+C-MAPA\s*\.?\s*$',
                        ln, re.IGNORECASE)
        if mred:
            saida.append(mred.group(1) + '.')
            i += 1
            continue

        # (6) Literal truncado "'DEAD*GOX*" -> "'DEADLOCK'" (ver docstring)
        mliteral = re.match(r"^(.*)'DEAD\*GOX\*\s*$", ln)
        if mliteral:
            nova = mliteral.group(1) + "'DEADLOCK'"
            if len(nova) > 72:
                # colapsa espacos multiplos so na area de codigo (col 8+) -
                # nunca mexe nas colunas 1-7 (sequencia/indicador do formato
                # fixo), senao desalinha o indicador e quebra a compilacao.
                nova = nova[:7] + re.sub(r' {2,}', ' ', nova[7:])
            if len(nova) <= 72:
                saida.append(nova + (' ' * (72 - len(nova))) + '*GOX*')
                i += 1
                continue

        # (3) SELECT X ASSIGN TO X -> SELECT X ASSIGN TO "X"
        self_assign = False

        def _quote_assign(m):
            nonlocal self_assign
            nome1, mid, nome2 = m.group(1), m.group(2), m.group(3)
            if nome1.upper() == nome2.upper():
                self_assign = True
                return f'SELECT {nome1}{mid}"{nome2}"'
            return m.group(0)

        ln2 = re.sub(r'(?i)SELECT\s+([A-Za-z][\w-]*)(\s+ASSIGN\s+TO\s+)([A-Za-z][\w-]*)',
                     _quote_assign, ln)
        if self_assign and usa_invalid_key:
            # linha NOVA (nao concatenada) para nao estourar a coluna 72 do
            # formato fixo - concatenar inline truncaria o texto em col 72.
            saida.append(ln2)
            saida.append('           ORGANIZATION IS RELATIVE')
            i += 1
            continue

        # (4) PERFORM X OF Y-STBG orfao (residuo de navegacao DMS)
        if re.match(r'^\s*PERFORM\s+[A-Za-z][\w-]*\s+OF\s+[A-Za-z][\w-]*-STBG\s*\.\s*$',
                    ln2, re.IGNORECASE):
            saida.append(_comment_line(ln2))
            i += 1
            continue

        saida.append(ln2)
        i += 1
    return '\n'.join(saida)


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
            # Comentar linhas orfas (continuacoes de linhas ja comentadas)
            # Padrao: linha anterior comentada, linha atual comeca com USING/INTO/FROM/etc
            if len(result) > 0 and result[-1][6:7] == '*':
                stripped = line.strip().upper()
                if stripped and stripped.split()[0] in ('USING', 'INTO', 'FROM', 'WHERE',
                        'ORDER', 'AND', 'OR', 'SET', 'VALUES', 'BY'):
                    result.append(_comment_line(line))
                    i += 1
                    continue

            # Comentar PERFORMs e CALLs de paragrafos de DB (Micro Focus syntax)
            if 'PERFORM' in line.upper() or 'CALL' in line.upper():
                upper_line = line.upper().strip()
                # Rotinas de TERMINACAO fatal (DMS aborta o run-unit nesse ponto no
                # mainframe real): virar CONTINUE (no-op) faz o controle voltar e
                # o loop que esperava o abend nunca terminar - trava para sempre
                # gerando saida infinita (visto em FGAT006D/FGAT030D). Precisa
                # realmente encerrar a execucao (GOBACK), nao so pular a linha.
                termina_run_unit = any(x in upper_line for x in [
                        'DATABASE-TERMINATE', 'HANDLE-DMTERMINATE',
                        'SYSTEM  DMTERMINATE', 'SYSTEM DMTERMINATE'])
                eh_dm_generico = termina_run_unit or any(x in upper_line for x in [
                        'DATABASE-OPEN', 'DATABASE-CLOSE', 'HANDLE-SQL',
                        '-STEN', ':TRUE)'])
                if eh_dm_generico:
                    result.append(_comment_line(line))
                    tem_ponto = (line.strip().endswith('.') or 'END-EXEC.' in line.upper())
                    if tem_ponto:
                        code_area = line[6:72] if len(line) > 72 else line[6:]
                        tem_ponto = code_area.rstrip().endswith('.')
                    if termina_run_unit:
                        result.append('           MOVE 99 TO RETURN-CODE')
                        result.append('           GOBACK.' if tem_ponto else '           GOBACK')
                    else:
                        result.append('           CONTINUE.' if tem_ponto else '           CONTINUE')
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
        # NAO gerar se WSGL-DATASETS.cpy existe (copybooks completos disponiveis)
        master_cpy = Path(output_path).parent / 'copy' / 'WSGL-DATASETS.cpy'
        if master_cpy.exists():
            host_vars = set()  # Copybooks ja definem tudo
        else:
            host_vars = set(re.findall(r':([A-Za-z][\w-]*)', content))

        # Reparos seguros de conversao (hoje: REDEFINES C-MAPA orfao)
        content = _reparar_literais_partidos(content)

        # Processar SQL
        processed = preprocessar_sql(content)

        # Se WSGL-DATASETS existe, nao precisa de -TABLES.cpy nem host vars
        master_cpy = Path(output_path).parent / 'copy' / 'WSGL-DATASETS.cpy'
        if not master_cpy.exists():
            # Adicionar COPY de table stubs (modo antigo)
            table_copy = f'       COPY {source_path.stem}-TABLES.\n'
            table_cpy = Path(output_path).parent / 'copy' / f'{source_path.stem}-TABLES.cpy'
            if table_cpy.exists():
                for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
                    if marker in processed:
                        processed = processed.replace(marker, table_copy + marker, 1)
                        break
                host_vars = set()

            # Adicionar declaracoes de host variables no WORKING-STORAGE
            if host_vars:
                var_decls = _gerar_host_vars(host_vars, content)
                inserted = False
                for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
                    if marker in processed:
                        processed = processed.replace(marker, var_decls + '\n' + marker, 1)
                        inserted = True
                        break
                if not inserted:
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
