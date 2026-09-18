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
from __future__ import annotations

import re
from pathlib import Path

_MAPAS_TELA_CACHE: set | None = None


def _mapas_tela(copy_dir: Path) -> set:
    """Nomes (sem extensao, maiusculo) dos copybooks em copy_dir que
    declaram '01 X REDEFINES C-MAPA' - as telas de terminal (BMS/TIP) que
    varios programas CICS compartilham o mesmo buffer C-MAPA. Cacheado
    (o conjunto de copybooks disponiveis nao muda durante o processo)."""
    global _MAPAS_TELA_CACHE
    if _MAPAS_TELA_CACHE is None:
        nomes = set()
        if copy_dir.is_dir():
            for f in copy_dir.glob('*.cpy'):
                try:
                    txt = f.read_text(encoding='latin-1', errors='ignore')
                except Exception:
                    continue
                # so' conta codigo de verdade (col 7 != '*'/'/') - senao um
                # comentario que so' MENCIONA "REDEFINES C-MAPA" (como este
                # aqui, ou o de WSGL.cpy) classificaria o proprio copybook
                # errado como tela.
                codigo = '\n'.join(ln for ln in txt.split('\n')
                                    if not (len(ln) >= 7 and ln[6] in ('*', '/')))
                if re.search(r'(?i)REDEFINES\s+C-MAPA\b', codigo):
                    nomes.add(f.stem.upper())
        _MAPAS_TELA_CACHE = nomes
    return _MAPAS_TELA_CACHE


def _agrupar_copies_mapa_tela(content: str, copy_dir: Path) -> str:
    """Move os 'COPY <mapa>.' de copybooks de tela (01 X REDEFINES C-MAPA)
    para logo apos 'COPY WSGL.' (onde C-MAPA e' declarado por ultimo de
    proposito - ver comentario em cobol_build/copy/WSGL.cpy).

    COBOL exige que um REDEFINES venha IMEDIATAMENTE apos o item original,
    sem nenhum outro 01-level no meio. Cada programa CICS usa varias telas
    (uma por transacao que trata), cada uma copiada no ponto do codigo que
    a usa - ou seja, espalhadas pelo fonte, nunca adjacentes ao C-MAPA nem
    umas as outras. Sem esse reagrupamento, o compilador rejeita com
    'REDEFINES must follow the original definition' assim que o programa
    referencia mais de uma tela (o caso comum - a maioria trata varias
    transacoes num so' dispatcher). Mover COPY statements nao muda logica
    nenhuma: e' so' inclusao textual em tempo de compilacao.
    """
    mapas = _mapas_tela(copy_dir)
    if not mapas:
        return content
    linhas = content.split('\n')

    relocadas = []
    mantidas = []
    for ln in linhas:
        m = re.match(r'(?i)^\s*COPY\s+([A-Za-z0-9\-]+)\b', ln)
        if m and m.group(1).upper() in mapas:
            relocadas.append(ln)
        else:
            mantidas.append(ln)
    if not relocadas:
        return content

    idx_wsgl = next((i for i, ln in enumerate(mantidas)
                      if re.match(r'(?i)^\s*COPY\s+WSGL\b', ln)), None)
    if idx_wsgl is None:
        return content  # sem COPY WSGL. - C-MAPA nao viria de la' mesmo
    mantidas[idx_wsgl + 1:idx_wsgl + 1] = relocadas
    return '\n'.join(mantidas)


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


def _stub_sql(texto_bloco_upper: str, tem_ponto: bool, nome_programa: str | None = None,
               marcar_cenario: list | None = None) -> str:
    """Escolhe o stub para um bloco EXEC SQL neutralizado, de acordo com o
    verbo usado - sem isso, todo bloco virava CONTINUE puro e DMSTATUS-S
    nunca mudava de valor. Dois problemas praticos disso: (1) um FETCH
    "sem mais linhas" nunca sinalizava NOTFOUND, entao um loop tipo
    'PERFORM ... UNTIL DMSTATUS-S = "NOTFOUND"' (ou uma flag derivada dele)
    ficava preso reprocessando a mesma linha (nunca atualizada) para
    sempre - travamento real visto em FGAT006D/FGAT030D; (2) um OPEN nunca
    sinalizava OK, entao o codigo que abre a tabela sempre caia no
    tratamento de erro, mesmo sem nenhuma relacao com os dados de teste
    (visto em FGAA012D/032D/050D/115D/FGEV006D - "ERRO ABERTURA X").

    Depende de DMSTATUS-S caber "NOTFOUND" (8 chars) - ver o tamanho do
    campo em cobol_build/copy/WSGLDB.cpy.

    Quando um FETCH corresponde a um cursor com cenarios de teste
    cadastrados (app/cenarios_teste.py), o stub vira um EVALUATE que le a
    variavel de ambiente COB_CENARIO em runtime: se bater um cenario
    conhecido PARA ESSE cursor especifico, simula "encontrado" com os
    campos daquele cenario (permite o programa calcular de verdade um
    resultado como "1 - Roubo" em vez de sempre "0 - nada consta");
    senao, simula NOTFOUND como no caso generico. `marcar_cenario`, se
    fornecido, recebe True anexado quando esse caminho e' usado, para o
    chamador saber que precisa declarar WS-CENARIO-TESTE.
    """
    ponto = '.' if tem_ponto else ''
    if re.search(r'\bFETCH\b', texto_bloco_upper):
        regra = _achar_regra_cenario(nome_programa, texto_bloco_upper)
        if regra:
            # flag "ja usado" por OCORRENCIA fisica de FETCH, nao global ao
            # programa: alguns cursores (ex: QXACHASS em FGAA012D/032D) sao
            # implementados como DOIS FETCHs fisicos distintos em sequencia
            # (FNDAT-1 + FNDAT-2, ambos precisam simular "OK" na MESMA
            # chamada para o resultado ser calculado). Uma flag global
            # marcada pelo 1o FETCH fazia o 2o (mesmo cursor, mesmo cenario)
            # ver "ja usado" e responder NOTFOUND, quebrando o resultado -
            # cada ocorrencia precisa da sua propria flag independente.
            idx_ocorrencia = len(marcar_cenario) if marcar_cenario is not None else 0
            flag = 'WS-CENARIO-JA-USADO-%d' % idx_ocorrencia
            if marcar_cenario is not None:
                marcar_cenario.append(True)
            # A flag em si (por ocorrencia) continua necessaria pra FETCHs
            # que SAO chamados repetidamente em loop pela MESMA ocorrencia
            # (ex: "FETCH NEXT" dentro de PERFORM ... UNTIL CH-NOTFOUND = "S"
            # em FGAT006D/FGAT030D) - sem ela, simular "OK" sempre que o
            # cenario bate faz o loop achar o "mesmo" registro pra sempre.
            linhas = [
                '           ACCEPT WS-CENARIO-TESTE FROM ENVIRONMENT "COB_CENARIO"',
                '           IF %s NOT = "S"' % flag,
                '               EVALUATE WS-CENARIO-TESTE',
            ]
            for codigo, campos in regra['cenarios'].items():
                linhas.append('                   WHEN "%s"' % codigo)
                linhas.append('                       MOVE "OK" TO DMSTATUS-S')
                linhas.append('                       MOVE "S" TO %s' % flag)
                # 'zerar': campos (tipicamente slots de uma tabela OCCURS,
                # ex: AX-RET-BLOQ(1..6)) que o programa testa com
                # "IF campo = ZEROS" pra saber se ainda estao livres. No
                # mainframe real esses slots chegam "vazios" via MOVE SPACES
                # (move de grupo) e essa comparacao numerica ainda da' certo;
                # no GnuCOBOL deste ambiente, SPACES movido pra um campo
                # PIC 9 nao e' igual a ZEROS numericamente (confirmado por
                # teste isolado) - sem isso o programa nunca considera o
                # slot livre e o cenario simulado nunca chega ao campo de
                # saida, mesmo com DMSTATUS-S = "OK".
                for campo in regra.get('zerar', ()):
                    linhas.append('                       MOVE ZEROS TO %s' % campo)
                for campo, valor in campos.items():
                    linhas.append('                       MOVE "%s" TO %s' % (valor, campo))
            linhas.append('                   WHEN OTHER')
            linhas.append('                       MOVE "NOTFOUND" TO DMSTATUS-S')
            linhas.append('               END-EVALUATE')
            linhas.append('           ELSE')
            linhas.append('               MOVE "NOTFOUND" TO DMSTATUS-S')
            linhas.append('           END-IF' + ponto)
            return '\n'.join(linhas)
        return '           MOVE "NOTFOUND" TO DMSTATUS-S' + ponto
    if re.search(r'\bOPEN\b', texto_bloco_upper):
        return '           MOVE "OK" TO DMSTATUS-S' + ponto
    return '           CONTINUE' + ponto


def _achar_regra_cenario(nome_programa: str | None, texto_bloco_upper: str):
    """Acha, em cenarios_teste.CENARIOS, a regra do programa cujo
    fragmento de nome de cursor aparece no texto deste bloco FETCH."""
    if not nome_programa:
        return None
    try:
        from cenarios_teste import CENARIOS
    except ImportError:
        from app.cenarios_teste import CENARIOS  # type: ignore
    for regra in CENARIOS.get(nome_programa.upper(), []):
        if regra['cursor'] in texto_bloco_upper:
            return regra
    return None


def preprocessar_sql(source_content: str, nome_programa: str | None = None) -> str:
    """
    Remove blocos EXEC SQL/CICS do fonte COBOL, substituindo por stubs.
    Preserva nomes de paragrafos que precedem EXEC SQL.
    Blocos antes da PROCEDURE DIVISION sao apenas comentados.
    Blocos na PROCEDURE DIVISION recebem CONTINUE.

    'nome_programa', se fornecido, habilita os stubs de FETCH a simular
    cenarios de teste especificos (ver cenarios_teste.py) quando a
    variavel de ambiente COB_CENARIO for setada em runtime.
    """
    lines = source_content.split('\n')
    result = []
    in_exec_sql = False
    exec_sql_lines = []
    bloco_eh_sql = False
    in_procedure_div = False
    usou_cenario = []

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
                    tem_ponto = (('.' in code_area and code_area.strip().rstrip().endswith('.'))
                                 or 'END-EXEC.' in line.upper())
                    is_sql = 'EXEC SQL' in line.upper()
                    result.append(_stub_sql(line.upper(), tem_ponto, nome_programa, usou_cenario) if is_sql
                                  else ('           CONTINUE.' if tem_ponto else '           CONTINUE'))
                i += 1
                continue
            in_exec_sql = True
            bloco_eh_sql = 'EXEC SQL' in line.upper()
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
                    tem_ponto = 'END-EXEC.' in last_line.upper() or code_area.rstrip().endswith('.')
                    if bloco_eh_sql:
                        texto_bloco = ' '.join(exec_sql_lines).upper()
                        result.append(_stub_sql(texto_bloco, tem_ponto, nome_programa, usou_cenario))
                    else:
                        result.append('           CONTINUE.' if tem_ponto else '           CONTINUE')
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

            # CALLs a rotinas de sistema Unisys ClearPath que nao existem
            # neste ambiente ("module X not found" em runtime - so' aparece
            # ao rodar de verdade, o programa compila normalmente porque a
            # resolucao de CALL por literal e' so' em tempo de execucao):
            #   - ENABLEX/DISABLEX: configuram/desligam timeout de leitura de
            #     terminal - infraestrutura pura, sem efeito em logica de
            #     negocio.
            #   - SENDX/RECEIVEX: enviam/recebem mensagem de um sistema
            #     remoto (ex: RENAVAM/BIN) por um buffer proprio (nao e' o
            #     C-MAPA da tela local) - equivalente a um FETCH de DB2 sem
            #     banco real: simula "completou sem erro" limpando o campo
            #     de status (ultimo parametro do USING, testado logo depois
            #     com "IF ... = 'X'" pra decidir abortar) - a logica real de
            #     negocio roda sobre o buffer de resposta vazio (= "nao
            #     encontrado", igual ao FETCH neutralizado).
            #   - DIGITCPF/DIGITCGC: validador de digito verificador de
            #     CPF/CNPJ (rotina separada, nao entre os fontes entregues) -
            #     simula "digito valido" (AX-LIB-DC-CONS = 1) pra nao travar
            #     essa checagem especifica; a validacao de digito em si fica
            #     fora do escopo do teste (nao temos o algoritmo real).
            # A clausula USING pode vir na(s) linha(s) seguinte(s) (sem ponto
            # final na propria linha do CALL) - consome ate' achar o ponto.
            m_syscall = re.match(
                r"(?i)^\s*CALL\s+['\"](ENABLEX|DISABLEX|SENDX|RECEIVEX|DIGITCPF|DIGITCGC)['\"]", line)
            if m_syscall:
                rotina = m_syscall.group(1).upper()
                result.append(_comment_line(line))
                tem_ponto_proprio = line.strip().endswith('.')
                linhas_using = [line]
                i += 1
                if not tem_ponto_proprio:
                    while i < len(lines) and not lines[i].strip().endswith('.'):
                        linhas_using.append(lines[i])
                        result.append(_comment_line(lines[i]))
                        i += 1
                    if i < len(lines):
                        linhas_using.append(lines[i])
                        result.append(_comment_line(lines[i]))
                        i += 1
                if rotina in ('SENDX', 'RECEIVEX'):
                    texto = ' '.join(l.strip() for l in linhas_using).upper()
                    mcampo = re.search(r'([A-Z][\w-]*)\s*\.\s*$', texto)
                    result.append('           MOVE SPACES TO %s.' % mcampo.group(1)
                                  if mcampo else '           CONTINUE.')
                elif rotina in ('DIGITCPF', 'DIGITCGC'):
                    result.append('           MOVE 1 TO AX-LIB-DC-CONS.')
                else:
                    result.append('           CONTINUE.')
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
                # PERFORM DATABASE-OPEN/TRANSACTION-BEGIN sempre e' seguido
                # de 'IF DMSTATUS-S NOT = "OK"' (confirmado em FGAA012D/032D/
                # 050D/115D, FGAT006D/030D, FGEV006D - mesmo padrao em
                # todos; TRANSACTION-BEGIN e' o mesmo padrao usado em 25
                # programas CICS pra abrir escopo de transacao antes de um
                # UPDATE, ex: OGAA013D/018D/640D/920D/PGAA100D). Virar
                # CONTINUE puro deixa DMSTATUS-S no default da WORKING-
                # STORAGE ("00", nunca "OK"), entao esse IF da erro em
                # 100% das execucoes, mesmo sem relacao nenhuma com os
                # dados de teste - nao e' "tabela nao existe para este
                # chassi", e' a abertura nunca sendo marcada como sucedida.
                # Simula um OPEN/BEGIN bem-sucedido (equivalente a "tabela
                # abriu, vazia") para o programa seguir ate' a logica real de
                # FETCH/cursor, que ja' costuma tratar "nao encontrado"
                # graciosamente (ex: DMSTATUS-S = 'NOTFOUND' em FGAT030D).
                abre_database = ('DATABASE-OPEN' in upper_line or 'TRANSACTION-BEGIN' in upper_line
                                  or 'TRANSACTION-END' in upper_line)
                eh_dm_generico = termina_run_unit or abre_database or any(x in upper_line for x in [
                        'DATABASE-CLOSE', 'HANDLE-SQL', '-STEN', ':TRUE)'])
                if eh_dm_generico:
                    result.append(_comment_line(line))
                    tem_ponto = (line.strip().endswith('.') or 'END-EXEC.' in line.upper())
                    if tem_ponto:
                        code_area = line[6:72] if len(line) > 72 else line[6:]
                        tem_ponto = code_area.rstrip().endswith('.')
                    if termina_run_unit:
                        result.append('           MOVE 99 TO RETURN-CODE')
                        result.append('           GOBACK.' if tem_ponto else '           GOBACK')
                    elif abre_database:
                        result.append('           MOVE "OK" TO DMSTATUS-S' + ('.' if tem_ponto else ''))
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

    if usou_cenario:
        # Pelo menos um stub de FETCH usou WS-CENARIO-TESTE (ACCEPT FROM
        # ENVIRONMENT "COB_CENARIO") - precisa declarar o campo, mais uma
        # flag "ja usado" POR OCORRENCIA (ver comentario em _stub_sql).
        # Injeta logo apos WORKING-STORAGE SECTION (mesmo padrao ja usado
        # em app/cobol_runner.py para variaveis auto-inferidas).
        for idx, ln in enumerate(result):
            if re.match(r'(?i)^\s*WORKING-STORAGE\s+SECTION\b', ln):
                for n in range(len(usou_cenario) - 1, -1, -1):
                    result.insert(idx + 1,
                                  '       01  WS-CENARIO-JA-USADO-%d      PIC X(001) VALUE SPACES.' % n)
                result.insert(idx + 1, '       01  WS-CENARIO-TESTE         PIC X(020) VALUE SPACES.')
                break

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
        content = _agrupar_copies_mapa_tela(content, Path(output_path).parent / 'copy')

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
        processed = preprocessar_sql(content, source_path.stem)

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
