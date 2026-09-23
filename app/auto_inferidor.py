"""
Auto-inferidor de simbolos/copybooks COBOL ausentes.

Quando um programa convertido nao compila porque copybooks de tabela/tela do
mainframe nao foram entregues (viram stubs vazios), este modulo:
  1. le os erros do cobc ("X is not defined") do fonte processado;
  2. analisa COMO cada simbolo e usado no proprio fonte (MOVEs, comparacoes,
     indices/OCCURS, host vars SQL, GO TO/PERFORM) para INFERIR um PIC razoavel;
  3. grava um copybook de inferencia por programa (INFER_<PROG>.cpy) com a marca
     '@inferido:' e injeta um COPY dele no fonte processado;
  4. deixa o compilar_modulo recompilar; o processo repete ate compilar ou
     atingir um limite de iteracoes.

A inferencia e uma APROXIMACAO (tipos/tamanhos deduzidos do uso). O objetivo e
permitir compilar/executar o teste; nao substitui o copybook original do DB2.
"""
from __future__ import annotations

import re
from pathlib import Path

# Palavras COBOL que nunca sao "variaveis a declarar" (evita falso positivo)
_PALAVRAS_RESERVADAS = {
    'SPACES', 'SPACE', 'ZEROS', 'ZERO', 'ZEROES', 'LOW-VALUES', 'HIGH-VALUES',
    'QUOTES', 'NULL', 'NULLS', 'TRUE', 'FALSE', 'THRU', 'THROUGH',
}


def _identificador_cobol_valido(n: str) -> bool:
    """Palavra de usuario COBOL valida: letras/digitos/hifen, sem hifen nas
    pontas, e com PELO MENOS uma letra (senao seria um numero, nao um nome).

    Importante: COBOL permite identificador comecando por DIGITO (ex:
    '1ST-CO04PLAC' e um nome real e comum nestes fontes) - um regex que exija
    letra no primeiro caractere descarta esses nomes silenciosamente.
    """
    if not n or n.startswith('-') or n.endswith('-'):
        return False
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9\-]*', n):
        return False
    return re.search(r'[A-Za-z]', n) is not None


def extrair_undefined(stderr: str) -> list:
    """Extrai nomes 'X is not defined' do stderr do cobc (nomes COBOL validos).

    Trata tambem referencias qualificadas 'X IN Y' / 'X OF Y' (pega o X, que e
    o item que falta) e ignora o qualificador Y.
    """
    brutos = set(re.findall(r"'([^']+)' is not defined", stderr or ''))
    validos = []
    for bruto in brutos:
        n = bruto.strip()
        # referencia qualificada: "CAMPO IN GRUPO" / "CAMPO OF GRUPO" -> pega CAMPO
        m = re.match(r'^([A-Za-z0-9][A-Za-z0-9\-]*)\s+(?:IN|OF)\s+[A-Za-z0-9]', n, re.IGNORECASE)
        if m:
            n = m.group(1)
        if not n or ' ' in n:
            continue
        if n.upper() in _PALAVRAS_RESERVADAS:
            continue
        if _identificador_cobol_valido(n):
            validos.append(n)
    return sorted(set(validos))


def extrair_qualificados(stderr: str) -> dict:
    """Mapeia 'X IN Y' / 'X OF Y' -> {Y_MAIUSC: {"nome": Y, "membros": {X,...}}}.

    Quando X so aparece qualificado por um grupo Y que nao existe (ex: campos
    de um pseudo-registro do ambiente como MYSELF do COMS Unisys, ou um alias
    de dataset tipo NOVAPLAC2), declarar X isolado nao resolve: o compilador
    exige que Y exista e que X esteja aninhado dentro dele. Agrupa por Y para
    permitir gerar um '01 Y' com os '05 X' correspondentes.
    """
    grupos: dict = {}
    for m in re.finditer(r"'([A-Za-z0-9][\w-]*)\s+(?:IN|OF)\s+([A-Za-z0-9][\w-]*)' is not defined",
                          stderr or '', re.IGNORECASE):
        x, y = m.group(1), m.group(2)
        chave = y.upper()
        grupos.setdefault(chave, {"nome": y, "membros": set()})["membros"].add(x)
    return grupos


def _tok(nome: str) -> str:
    """Escapa e delimita um identificador COBOL para uso em regex.

    Identificadores COBOL contem hifen (ex: QUEIXADS-DB2DMS), mas \\b do Python
    trata '-' como nao-palavra: \\bQUEIXADS\\b casaria dentro de
    'QUEIXADS-DB2DMS' ou 'PREFIXO-QUEIXADS'. Usa lookaround exigindo que os
    vizinhos nao sejam letra/digito/hifen, para so casar o identificador
    inteiro isoladamente.
    """
    return r'(?<![A-Za-z0-9-])' + re.escape(nome) + r'(?![A-Za-z0-9-])'


def _extrair_alvos_perform_goto(codigo: str) -> set:
    """Uma unica varredura O(linhas): nomes usados como alvo de GO TO / PERFORM.

    Mesma razao de _extrair_moves/_extrair_declaracoes_numericas: sem isso,
    _eh_paragrafo varria o fonte inteiro POR SIMBOLO ausente. Em arquivos que
    tinham muitos identificadores digit-first descartados pelo bug antigo de
    extrair_undefined, o numero de simbolos ausentes de uma vez pode ser
    enorme (milhares) - travando o auto-inferidor por muito mais que o
    orcamento de tempo numa unica iteracao (caso do OGAA013D).
    """
    return {m.group(1).upper()
            for m in re.finditer(r'(?i)\b(?:GO\s+TO|GO|PERFORM)\s+([A-Za-z0-9][\w-]*)', codigo)}


def _extrair_alvos_to(codigo: str) -> set:
    """Uma unica varredura O(linhas): nomes usados como alvo 'TO <nome>'."""
    return {m.group(1).upper()
            for m in re.finditer(r'(?i)\bTO\s+([A-Za-z0-9][\w-]*)', codigo)}


def _extrair_indexados(codigo: str) -> set:
    """Uma unica varredura O(linhas): nomes usados com indice NOME(...)."""
    return {m.group(1).upper()
            for m in re.finditer(r'([A-Za-z][\w-]*)\s*\(', codigo)}


def _eh_paragrafo(nome: str, codigo: str, alvos_perform: set | None = None,
                   alvos_to: set | None = None) -> bool:
    """Heuristica: o nome e um paragrafo (label) e nao uma variavel?

    E paragrafo se aparece como alvo de GO TO / PERFORM, ou se casa com o
    padrao tipico de nomes de paragrafo do conversor (ex: 999-..., -DB2DMS).

    'alvos_perform'/'alvos_to', se fornecidos (pre-calculados 1x por
    gerar_copybook_inferido), evitam re-varrer o fonte inteiro a cada nome.
    """
    u = nome.upper()
    if u.startswith('HANDLE-') or u.startswith('DATABASE-') or u.endswith('-DB2DMS'):
        return True
    # numero-prefixado (000-, 030-E-, 9999-...) tipico de secao/paragrafo.
    # Exige que o trecho antes do hifen seja so digitos (evita falso positivo
    # em campos como '1ST-CO04PLAC', onde '1ST' nao e numero de paragrafo).
    if re.match(r'^\d+-', nome):
        return True
    # alvo de GO TO / PERFORM no codigo
    eh_alvo = (u in alvos_perform) if alvos_perform is not None else \
        bool(re.search(r'(?i)\b(GO\s+TO|GO|PERFORM)\s+' + _tok(nome), codigo))
    if eh_alvo:
        # mas so se NAO for usado como dado (MOVE ... TO nome / nome comparado)
        recebe_dado = (u in alvos_to) if alvos_to is not None else \
            bool(re.search(r'(?i)\bTO\s+' + _tok(nome), codigo))
        if not recebe_dado:
            return True
    return False


def _tem_indice(nome: str, codigo: str, indexados: set | None = None) -> bool:
    """O campo e usado com indice? Ex: NOME(1), NOME(IX1) -> precisa OCCURS."""
    if indexados is not None:
        return nome.upper() in indexados
    return re.search(_tok(nome) + r'\s*\(', codigo) is not None


def _extrair_operandos_aritmeticos(codigo: str) -> set:
    """Identificadores usados como operando de COMPUTE/ADD/SUBTRACT/MULTIPLY/DIVIDE.

    Uma unica varredura O(linhas) do fonte inteiro (nao por nome): coleta todos
    os tokens dentro de cada statement aritmetico (verbo ate o ponto final,
    pois COMPUTE costuma quebrar em varias linhas no formato fixo).
    """
    operandos = set()
    dentro = False
    for ln in codigo.split('\n'):
        if len(ln) >= 7 and ln[6] in ('*', '/'):
            continue
        area_b = ln[7:72] if len(ln) > 7 else ln
        if not dentro and re.search(r'(?i)\b(COMPUTE|ADD|SUBTRACT|MULTIPLY|DIVIDE)\b', area_b):
            dentro = True
        if dentro:
            for tokm in re.finditer(r'[A-Za-z][A-Za-z0-9-]*', area_b):
                operandos.add(tokm.group(0).upper())
            if area_b.rstrip().endswith('.'):
                dentro = False
    return operandos


_VERBOS_PARADA = {
    'MOVE', 'IF', 'ELSE', 'END-IF', 'PERFORM', 'ADD', 'SUBTRACT', 'MULTIPLY',
    'DIVIDE', 'COMPUTE', 'GO', 'DISPLAY', 'READ', 'WRITE', 'CALL', 'STOP',
    'EXIT', 'NEXT', 'GOBACK', 'STRING', 'UNSTRING', 'INITIALIZE', 'SET',
}
_RE_MOVE_TO = re.compile(r'(?i)\bMOVE\s+(SPACES?|LOW-VALUES?|[A-Za-z][\w-]*)\s+TO\s+')
_RE_TOKEN_OU_PONTO = re.compile(r'[A-Za-z][\w-]*|\.')


def _extrair_moves(codigo: str) -> dict:
    """Uma unica varredura O(linhas) para tudo que _inferir_pic precisaria
    buscar por 'MOVE ... TO <campo>' - sem isso, cada um dos N simbolos
    ausentes fazia sua propria busca no fonte inteiro (O(N x tamanho do
    fonte)), o que em arquivos grandes com centenas de simbolos (ex:
    OGAA640D) trava o auto-inferidor por minutos numa unica iteracao,
    sem respeitar o orcamento de tempo (que so e checado ENTRE iteracoes).

    Retorna {"origens_por_alvo": {ALVO: [origem,...]}, "recebe_espacos": {ALVO,...}}.

    MOVE pode ter VARIOS alvos numa frase so ("MOVE SPACES TO A B C D."),
    inclusive quebrando linha no formato fixo sem hifen de continuacao -
    por isso os alvos sao coletados token a token (nao por findall numa
    unica captura) ate o ponto final ou um verbo COBOL reconhecido.

    IMPORTANTE: a lista de alvos era antes capturada por um grupo regex
    repetido {1,20} (para nao vazar para a sentenca seguinte). Um MOVE com
    MAIS de 20 alvos antes do ponto (comum em fontes gerados por conversor,
    ex: OGAA013D com 30+ alvos por MOVE) faz esse grupo falhar em 20 alvos,
    tentar 19, 18... 1 - e o backtracking de duas quantificacoes adjacentes
    ([\\w-]* seguido de [\\s,]*) dentro de cada uma dessas ~20 tentativas
    explode combinatoriamente (trava minutos/horas numa unica chamada, sem
    excecao nem timeout, ja que e trabalho puro de regex, nao subprocesso).
    Por isso os alvos agora sao coletados com finditer token-a-token (sem
    quantificador limitado, sem backtracking possivel).

    Cuidado: um MOVE dentro de 'IF ... MOVE X TO Y ELSE MOVE Z TO W.' nao
    tem ponto logo apos o seu proprio alvo (o ponto so fecha a sentenca IF
    inteira) - sem parar em outro verbo, a lista de alvos "vazava" para o
    ELSE/MOVE seguinte e atribuia o alvo errado a origem errada. Por isso a
    lista para no primeiro verbo COBOL reconhecido, nao so no ponto.
    """
    origens_por_alvo: dict = {}
    recebe_espacos = set()
    for m in _RE_MOVE_TO.finditer(codigo):
        origem = m.group(1)
        eh_espacos = origem.upper() in ('SPACE', 'SPACES', 'LOW-VALUE', 'LOW-VALUES')
        alvos = []
        for tokm in _RE_TOKEN_OU_PONTO.finditer(codigo, m.end()):
            tok = tokm.group(0)
            if tok == '.' or tok.upper() in _VERBOS_PARADA or len(alvos) >= 200:
                break
            alvos.append(tok)
        for alvo in alvos:
            alvo_up = alvo.upper()
            if eh_espacos:
                recebe_espacos.add(alvo_up)
            else:
                origens_por_alvo.setdefault(alvo_up, []).append(origem)
    return {"origens_por_alvo": origens_por_alvo, "recebe_espacos": recebe_espacos}


def _extrair_declaracoes_numericas(codigo: str) -> dict:
    """Uma unica varredura O(linhas): mapeia NOME_MAIUSC -> tem_decimais(bool)
    para toda declaracao REAL (nao comentada, nao inferida) com PIC numerica.
    """
    decls: dict = {}
    for ln in codigo.split('\n'):
        if len(ln) >= 7 and ln[6] in ('*', '/'):
            continue
        m = re.search(r'(?i)\b([A-Za-z][\w-]*)\s+PIC(?:TURE)?\s+(?:IS\s+)?(S?9[9,.\-()V]*)', ln)
        if m:
            decls[m.group(1).upper()] = ('V' in m.group(2).upper())
    return decls


def _extrair_moves_literal_numerico(codigo: str) -> set:
    """Uma unica varredura O(linhas): nomes que recebem 'MOVE <numero> TO nome'."""
    return {m.group(1).upper()
            for m in re.finditer(r'(?i)\bMOVE\s+[0-9]+\s+TO\s+([A-Za-z0-9][\w-]*)', codigo)}


def _extrair_comparados_numero(codigo: str) -> set:
    """Uma unica varredura O(linhas): nomes comparados com literal numerico
    (NOME = 0, NOME > 1993, etc)."""
    return {m.group(1).upper()
            for m in re.finditer(r'(?i)([A-Za-z][\w-]*)\s*(?:=|>|<|NOT\s*=|>=|<=)\s*[0-9]+\b', codigo)}


def _extrair_testados_numeric(codigo: str) -> set:
    """Uma unica varredura O(linhas): nomes testados com a condicao NUMERIC."""
    return {m.group(1).upper()
            for m in re.finditer(r'(?i)([A-Za-z][\w-]*)\s+(?:IS\s+)?NUMERIC\b', codigo)}


def _origem_move_numerica(nome: str, moves: dict, decls_numericas: dict) -> tuple:
    """O campo recebe 'MOVE origem TO nome' onde 'origem' tem declaracao REAL
    (nao inferida, nao comentada) com PIC numerica no fonte?

    Detecta casos como 'MOVE CRV-CAPCAR TO PLC-CAP-CAR' onde CRV-CAPCAR e
    'PIC 999V99 COMP' de verdade - se PLC-CAP-CAR (ausente) for inferido como
    alfanumerico, o MOVE numerico->alfanumerico de um COMP da erro no
    GnuCOBOL ('invalid MOVE statement'). Retorna (e_numerico, tem_decimais).
    Usa os mapas pre-calculados (uma vez por arquivo) em vez de varrer o
    fonte inteiro de novo para cada nome.
    """
    for origem in moves["origens_por_alvo"].get(nome.upper(), []):
        if origem.upper() in decls_numericas:
            return True, decls_numericas[origem.upper()]
    return False, False


def _inferir_pic(nome: str, codigo: str, aritmeticos: set | None = None,
                  moves: dict | None = None, decls_numericas: dict | None = None,
                  moves_literal: set | None = None, comparados: set | None = None,
                  testados_numeric: set | None = None) -> str:
    """Infere um PIC para uma variavel a partir do nome e do uso no codigo.

    Ordem: uso concreto (comparacao numerica, MOVE de literal numerico) tem
    prioridade; depois heuristica por nome; default X(030).

    Todos os parametros de conjunto/dict, se fornecidos (pre-calculados 1x
    por gerar_copybook_inferido), evitam re-varrer o fonte inteiro a cada
    campo - importante em fontes grandes com muitos simbolos ausentes (sem
    isso, um arquivo com milhares de simbolos ausentes - caso do OGAA013D
    apos o fix do bug de identificadores digit-first - trava o
    auto-inferidor por muito mais que o orcamento de tempo numa unica
    iteracao).
    """
    u = nome.upper()
    base = u[:-2] if u.endswith('-X') else u

    # 0) Nome de dataset (record de tabela): termina em DS -> area grande
    if base.endswith('DS'):
        return 'PIC X(200)'

    # 0.5) Evidencia NEGATIVA forte: recebe MOVE de SPACE(S)/LOW-VALUE(S) ->
    # so e legal em item alfanumerico. Tem prioridade sobre heuristica de
    # nome (ex: 'OBS-VLR-NUM' parece numerico pelo nome, mas recebe SPACES).
    recebe_espacos = (u in moves["recebe_espacos"]) if moves is not None else \
        bool(re.search(r'(?i)\bMOVE\s+(SPACE|SPACES|LOW-VALUE|LOW-VALUES)\s+TO\s+' + _tok(nome), codigo))
    if recebe_espacos:
        return 'PIC X(030)'

    # 1) Uso: comparado com numero ou recebe literal numerico -> numerico
    #    ex: "NOME = 0", "NOME > 1993", "MOVE 9999 TO NOME"
    if moves is not None and decls_numericas is not None:
        origem_numerica, origem_decimal = _origem_move_numerica(nome, moves, decls_numericas)
    else:
        origem_numerica, origem_decimal = False, False
    tem_move_literal = (u in moves_literal) if moves_literal is not None else \
        bool(re.search(r'(?i)\bMOVE\s+[0-9]+\s+TO\s+' + _tok(nome), codigo))
    tem_comparacao = (u in comparados) if comparados is not None else \
        bool(re.search(r'(?i)' + _tok(nome) + r'\s*(=|>|<|NOT\s*=|>=|<=)\s*[0-9]+\b', codigo))
    tem_numeric = (u in testados_numeric) if testados_numeric is not None else \
        bool(re.search(r'(?i)' + _tok(nome) + r'\s+(IS\s+)?NUMERIC\b', codigo))
    if tem_move_literal or tem_comparacao or tem_numeric \
       or (u in aritmeticos if aritmeticos is not None else False) \
       or origem_numerica:
        if origem_decimal:
            return 'PIC 9(007)V99'
        # campos de dominio com LARGURA FIXA conhecida: mesmo usados
        # numericamente, precisam do tamanho certo senao um MOVE de um campo
        # maior TRUNCA os digitos (ex: TAX-CPF-X 9(9) recebendo IN-CPF 9(11)
        # perdia os 2 digitos da esquerda e a consulta por CPF nunca casava).
        if ('CPF' in base and ('CGC' in base or 'CNPJ' in base)) or 'CNPJ' in base or 'CGC' in base:
            return 'PIC 9(014)'
        if 'CPF' in base:
            return 'PIC 9(011)'
        if 'RENAVAM' in base:
            return 'PIC 9(011)'
        # tamanho por nome (ano/codigo) ou default 9
        if 'ANO' in base:
            return 'PIC 9(004)'
        if any(x in base for x in ('COD', 'NUM', 'SEQ', 'QTD', 'IND', 'TIPO', 'SIT', 'STATU')):
            return 'PIC 9(005)'
        return 'PIC 9(009)'

    # 2) Heuristica por nome (campos textuais tipicos do dominio Detran)
    if 'ROWID' in base:
        return 'PIC X(040)'
    if 'CHASSI' in base:
        return 'PIC X(021)'
    if 'PLACA' in base:
        return 'PIC X(010)'
    if 'CPF' in base and ('CGC' in base or 'CNPJ' in base):
        return 'PIC X(014)'
    if 'CPF' in base:
        return 'PIC X(011)'
    if 'CNPJ' in base or 'CGC' in base:
        return 'PIC X(014)'
    if 'RENAVAM' in base:
        return 'PIC X(011)'
    if 'CEP' in base:
        return 'PIC X(008)'
    if base.endswith('-UF') or 'SIG-EST' in base:
        return 'PIC X(002)'
    if any(x in base for x in ('-DT-', '-DATA', '-DATE', 'DT-')):
        return 'PIC X(010)'
    if any(x in base for x in ('-HR-', '-HORA', 'HR-')):
        return 'PIC X(008)'
    if 'ANO' in base:
        return 'PIC 9(004)'
    if 'MUNIC' in base or 'MUN-' in base or 'MUNI' in base:
        return 'PIC 9(005)'
    if any(x in base for x in ('VALOR', 'VLR-', '-VLR', 'SALDO', 'PRECO')):
        return 'PIC 9(009)V99'
    if any(x in base for x in ('NOME', 'ENDER', 'DESCR', 'OBSERV', 'MENS', 'MENSAGEM')):
        return 'PIC X(050)'
    if any(x in base for x in ('COD', 'TIPO', 'CATEG', 'CLASS', 'ORIG', 'STATU', 'SIT')):
        return 'PIC X(006)'
    if 'USUARIO' in base or 'USU-' in base or base == 'USUARIO':
        return 'PIC X(008)'
    if 'CODE' in base:
        return 'PIC X(004)'
    if 'TERMINAL' in base:
        return 'PIC X(008)'
    # default: alfanumerico generico
    return 'PIC X(030)'


def gerar_copybook_inferido(nome_programa: str, undefined: list, codigo: str,
                            copy_dir: Path, qualificados: dict | None = None) -> tuple:
    """Gera/atualiza o copybook de inferencia do programa e retorna (caminho, resumo).

    resumo = {"campos": [...], "paragrafos": [...]}
    """
    qualificados = qualificados or {}

    # Conjunto de nomes JA definidos como item de dados em linhas NAO comentadas
    # (col 7 != '*'). Evita redeclarar (erro 'redefinition of') sem confundir
    # com definicoes que aparecem em linhas comentadas.
    definidos = set()
    for linha in codigo.split('\n'):
        if len(linha) >= 7 and linha[6] in ('*', '/'):
            continue  # comentario: nao conta como definicao
        m = re.match(r'^\s*\d{2}\s+([A-Za-z][A-Za-z0-9\-]*)', linha)
        if m:
            definidos.add(m.group(1).upper())

    # Nomes que so aparecem qualificados (X IN/OF Y): nao declarar soltos,
    # serao aninhados dentro do grupo Y logo abaixo. O proprio Y tambem nao
    # entra na lista solta (vira um '01 Y' com os membros dentro).
    membros_qualificados = set()
    for info in qualificados.values():
        membros_qualificados.update(m.upper() for m in info["membros"])

    # 1 varredura do fonte inteiro (nao 1 por campo - fontes tem milhares de
    # linhas e dezenas/centenas (as vezes milhares) de simbolos ausentes de
    # uma vez).
    aritmeticos = _extrair_operandos_aritmeticos(codigo)
    moves = _extrair_moves(codigo)
    decls_numericas = _extrair_declaracoes_numericas(codigo)
    alvos_perform = _extrair_alvos_perform_goto(codigo)
    alvos_to = _extrair_alvos_to(codigo)
    indexados = _extrair_indexados(codigo)
    moves_literal = _extrair_moves_literal_numerico(codigo)
    comparados = _extrair_comparados_numero(codigo)
    testados_numeric = _extrair_testados_numeric(codigo)

    def _pic(nome_campo: str) -> str:
        return _inferir_pic(nome_campo, codigo, aritmeticos, moves, decls_numericas,
                             moves_literal, comparados, testados_numeric)

    vars_ws = []      # (nome, pic, occurs)
    paragrafos = []
    for nome in undefined:
        # nao redeclarar algo ja definido como dado (em linha nao comentada)
        if nome.upper() in definidos:
            continue
        if nome.upper() in membros_qualificados or nome.upper() in qualificados:
            continue
        if _eh_paragrafo(nome, codigo, alvos_perform, alvos_to):
            paragrafos.append(nome)
        else:
            pic = _pic(nome)
            occurs = _tem_indice(nome, codigo, indexados)
            vars_ws.append((nome[:30], pic, occurs))

    linhas = []
    linhas.append('      *================================================================*')
    linhas.append('      * INFER_%s - Simbolos inferidos automaticamente' % nome_programa)
    linhas.append('      *')
    linhas.append('      * ATENCAO: Estes campos/paragrafos NAO vieram nos copybooks')
    linhas.append('      * originais do mainframe. Foram INFERIDOS a partir do uso no')
    linhas.append('      * codigo para permitir a compilacao/execucao do teste. Os tipos')
    linhas.append('      * e tamanhos sao APROXIMACAO e podem nao ser fieis ao DB2 original.')
    linhas.append('      *')
    linhas.append('      * @inferido: INFER_%s (simbolos deduzidos do uso)' % nome_programa)
    linhas.append('      *================================================================*')

    # Grupos qualificados (X IN/OF Y): 01 Y. / 05 X PIC ... (Y nao existe no
    # fonte - se ja existisse em linha nao comentada, o copybook real ja
    # resolveria e nao chegaria aqui como erro).
    grupos_gerados = []
    for chave, info in sorted(qualificados.items()):
        if chave in definidos:
            continue
        grupo_nome = info["nome"][:30]
        linhas.append('       01  %s.' % grupo_nome)
        for membro in sorted(info["membros"]):
            if membro.upper() in definidos:
                continue
            pic = _pic(membro)
            val = 'VALUE ZERO' if pic.strip().startswith('PIC 9') else 'VALUE SPACES'
            linhas.append('           05  %-26s %s %s.' % (membro[:26], pic, val))
        grupos_gerados.append(grupo_nome)

    # Bloco de dados (WORKING-STORAGE)
    for nome, pic, occurs in sorted(vars_ws):
        if occurs:
            # grupo com OCCURS para permitir indexacao NOME(i)
            linhas.append('       01  %-30s %s OCCURS 50 TIMES.' % (nome, pic))
        else:
            val = 'VALUE ZERO' if pic.strip().startswith('PIC 9') else 'VALUE SPACES'
            linhas.append('       01  %-30s %s %s.' % (nome, pic, val))

    cpy = copy_dir / ('INFER_%s.cpy' % nome_programa)
    cpy.write_text('\n'.join(linhas) + '\n', encoding='latin-1')

    campos = [v[0] for v in vars_ws] + grupos_gerados
    return cpy, {"campos": campos, "paragrafos": paragrafos}


def gerar_paragrafos_inferidos(nome_programa: str, paragrafos: list,
                               copy_dir: Path, codigo_proc: str | None = None) -> Path | None:
    """Gera um copybook de PROCEDURE com stubs de paragrafo (CONTINUE).

    Paragrafos '<TABELA>-LOCK' sao um padrao de DM (Unisys) pra travar um
    registro antes de atualizar - visto em dezenas de paragrafos assim
    (ex: PRODCRVDS-LOCK, GEVERDS-LOCK, BLOQUEIODS-LOCK) nos programas CICS
    "dispatcher" (OGAA013D/018D/640D/etc). Sempre sao seguidos de 'IF
    DMSTATUS-S NOT = "OK"' - um CONTINUE puro deixa DMSTATUS-S no default
    da WORKING-STORAGE (nunca "OK"), abortando a execucao ANTES de chegar
    em qualquer logica de negocio de verdade, mesmo sem relacao nenhuma
    com o dado de teste. Mesmo raciocinio ja aplicado a DATABASE-OPEN/
    TRANSACTION-BEGIN em sql_preprocessor.py - aqui e' o mesmo padrao, so'
    que o alvo e' um paragrafo inteiro (nao um EXEC SQL ou uma linha
    PERFORM reconhecida por texto fixo), entao o fix e' na propria geracao
    do stub.
    """
    if not paragrafos:
        return None
    linhas = []
    linhas.append('      * INFER_PD_%s - Paragrafos inferidos (stubs)' % nome_programa)
    linhas.append('      * @inferido: INFER_PD_%s (paragrafos deduzidos do uso)' % nome_programa)
    for p in sorted(paragrafos):
        linhas.append('       %s.' % p[:30])
        if p.upper().endswith('-LOCK'):
            linhas.append('           MOVE "OK" TO DMSTATUS-S.')
        else:
            linhas.append('           CONTINUE.')
    cpy = copy_dir / ('INFER_PD_%s.cpy' % nome_programa)
    cpy.write_text('\n'.join(linhas) + '\n', encoding='latin-1')
    return cpy


def injetar_copys(processed_path: Path, nome_programa: str,
                  tem_dados: bool, tem_paragrafos: bool) -> None:
    """Injeta os COPY dos copybooks inferidos no fonte processado.

    - dados: antes de LINKAGE SECTION ou PROCEDURE DIVISION
    - paragrafos: antes de COPY PDGL/PDGLDB, senao no final do arquivo
    """
    content = processed_path.read_text(encoding='latin-1', errors='ignore')

    if tem_dados and ('COPY INFER_%s' % nome_programa) not in content:
        copy_ws = '       COPY INFER_%s.\n' % nome_programa
        inserido = False
        for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
            if marker in content:
                content = content.replace(marker, copy_ws + marker, 1)
                inserido = True
                break
        if not inserido:
            # fallback: apos a primeira WORKING-STORAGE SECTION
            m = re.search(r'(?i)WORKING-STORAGE\s+SECTION\.', content)
            if m:
                idx = m.end()
                content = content[:idx] + '\n' + copy_ws + content[idx:]

    if tem_paragrafos and ('COPY INFER_PD_%s' % nome_programa) not in content:
        copy_pd = '       COPY INFER_PD_%s.\n' % nome_programa
        inserido = False
        for marker in ['       COPY PDGL', '       COPY PDGLDB']:
            if marker in content:
                content = content.replace(marker, copy_pd + marker, 1)
                inserido = True
                break
        if not inserido:
            content = content.rstrip() + '\n' + copy_pd

    processed_path.write_text(content, encoding='latin-1')
