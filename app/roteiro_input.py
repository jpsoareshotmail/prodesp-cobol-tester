"""
Injecao de entrada de roteiro nos programas "dispatcher" CICS.

Contexto: OGAA018D/OGAA920D/OGAA640D (e similares) nao recebem dado por
PROCEDURE DIVISION USING - a entrada chega por uma tela/mapa de transacao
(container COMS: C-MAPA / AREA-IN) que, no ambiente de teste, fica vazia
porque o proprio CONTAINER-GET (definido no copybook compartilhado PDGLDB)
e um stub CONTINUE.

Estrategia "A-minimo" (decidida com o usuario): logo APOS o
'PERFORM CONTAINER-GET THRU END-CONTAINER-GET' no fonte processado, injetamos
COBOL que POPULA os campos de chave do mapa (chassi/CPF/CNPJ) a partir das
variaveis de ambiente COB_CHASSI/COB_CPF/COB_CNPJ, e FORCA os campos de
controle da transacao (codigo/usuario) que funcionam como "portao" antes da
consulta real. Assim o valor do roteiro chega ao WHERE do EXEC SQL e a
consulta le o banco semeado de verdade (resultado passa a depender do dado:
achou vs nao-achou).

Fazemos isso no fonte processado (nao no CONTAINER-GET compartilhado) para o
efeito ser POR PROGRAMA - cada dispatcher tem seu mapa e seu portao. NAO
simula a tela inteira (dezenas de campos de consistencia), apenas o suficiente
para alcancar a primeira consulta data-dependent.

Cada campo referenciado e checado contra o fonte + copybooks ANTES de ser
emitido, para nunca gerar referencia a campo inexistente (que quebraria a
compilacao). Mapeamento explicito por programa (nao heuristico): lista curta
e auditavel.
"""
from __future__ import annotations

import re
from pathlib import Path


# Config por programa convertido.
#   map_moves: [(campo_do_mapa, envvar)] - ACCEPT do valor da env var pro campo
#   forcar:    [(campo, literal_cobol)]  - MOVE de um literal fixo (portao)
# Todos os campos sao verificados no fonte+copybooks antes de emitir (campos
# ausentes sao silenciosamente pulados).
CONFIG = {
    'OGAA018D': {
        'map_moves': [('CO02CHAS', 'COB_CHASSI'), ('CO02CPF', 'COB_CPF')],
        # GERACODE='CAV2' entra no dispatch da transacao; USUARIO/WS-USU perfil
        # valido ('DV') passa o filtro de perfil.
        'forcar': [('GERACODE', 'CAV2'), ('AX-GERACODE', 'CAV2'),
                   ('USUARIO', 'DV'), ('WS-USU', 'DV'), ('WS-USU2', 'DV')],
        # PORTAO de sessao: 030-E-HABILITA exige um registro de habilitacao de
        # terminal/usuario (PRODCRVDS por LSN-TERMINAL/USUARIO com data de hoje
        # e status != 0) que so' existe no mainframe - impossivel de satisfazer
        # aqui. Neutralizamos zerando IA1 logo apos o PERFORM de habilitacao,
        # antes do 'IF IA1 > 0 GO 020-90' que pularia toda a transacao.
        'apos_perform': [
            # apos a habilitacao, zera IA1 (portao de sessao) e RE-FORCA
            # GERACODE=CAV2 (a habilitacao NOTFOUND sobrescreve o campo de
            # controle - MENSCODE/DHAB - que compartilha storage com GERACODE
            # via redefinicao do C-MAPA), imediatamente antes do dispatch.
            (r'PERFORM\s+030-E-HABILITA\s+THRU\s+030-S-HABILITA\.',
             ['           MOVE 0 TO IA1',
              '           MOVE "CAV2" TO GERACODE']),
            # WS-AUXILIA=1 (contador de erro de I/O do ambiente COMS, sem
            # sentido fora do mainframe) faz GO 020-S-PROCESSA e sai; zera.
            (r'MOVE H-MAPA-E   TO C-HEADER\.',
             ['           MOVE 0 TO WS-AUXILIA']),
            # OBSERVABILIDADE: logo apos a consulta real GEVER por chassi,
            # expoe o sinal de negocio CH-NOT-GEVER (0=ficha encontrada no
            # GEVER / 1=nao encontrada) como 'RESULT=' - o driver de teste
            # le essa linha (ver cobol_runner._parsear_resultado_driver) e a
            # transforma no codigo do resultado. Assim o resultado observavel
            # passa a DEPENDER do dado semeado (chassi do roteiro achado ou
            # nao no banco), que e' o objetivo da validacao.
            (r'PERFORM 510-E-PESQ-GEVER        THRU    510-S-PESQ-GEVER\.',
             ['           DISPLAY "RESULT=" CH-NOT-GEVER']),
        ],
        # ARTEFATO DE CONVERSAO: logo apos o CONTAINER-GET ha um
        # 'MOVE TASKVALUE OF MYSELF TO WS-CONTIME / GO 020-S-PROCESSA.'
        # cuja condicao (IF STATUSVALUE OF COMS-IN invalido) foi COMENTADA na
        # conversao - o GO ficou INCONDICIONAL e faz o programa sair
        # imediatamente, antes de habilitacao/CAV2/consulta. Neutralizamos
        # trocando esse GO ativo por CONTINUE (a versao comentada *GOT* fica
        # intacta).
        'substituir': [
            (r'(?m)^             MOVE      TASKVALUE   OF  MYSELF\n'
             r'             TO      WS-CONTIME\n'
             r'             GO      020-S-PROCESSA\.',
             '             MOVE      TASKVALUE   OF  MYSELF\n'
             '             TO      WS-CONTIME\n'
             '      * INJECAO-ROTEIRO-INPUT: GO 020-S-PROCESSA neutralizado\n'
             '             CONTINUE.'),
            # 2o artefato: apos 'IF MAPA-E-S = "ENDEND" PERFORM 200-E-FINAL'
            # ha um 'PERFORM CONTAINER-RETURN ... / GOBACK.' que ficou
            # INCONDICIONAL na conversao (era o ramo de fim de sessao) e sai
            # do programa antes de qualquer transacao. Como MAPA-E-S nunca e'
            # "ENDEND" no teste, neutralizamos SO' esse GOBACK - ancorado no
            # 'STOP RUN' comentado + PERFORM 200-E-FINAL que o precede, para
            # nao acertar o CONTAINER-RETURN legitimo do fim do monitor.
            (r'(?m)^      \*             STOP    RUN\.                                           \*GOT\*\n'
             r'           PERFORM CONTAINER-RETURN THRU END-CONTAINER-RETURN\.             \*GOT\*\n'
             r'           GOBACK\.',
             '      *             STOP    RUN.                                           *GOT*\n'
             '      * INJECAO-ROTEIRO-INPUT: CONTAINER-RETURN/GOBACK incondicional neutralizado\n'
             '           CONTINUE.'),
        ],
    },
    'OGAA920D': {
        # 920D usa AREA-IN (IN-CODE='RAUT') com CPF em IN-CPFCGC/IN-CPF.
        # Dispatch: IF IN-CODE='RAUT' e IN-COD-SERVICO em {17..28} e
        # IN-SENHA-04 NUMERIC -> 300-E-TAXAS-NV -> 310-E-VERTAXA consulta
        # TAXADS por (TAX-TIPO=IN-COD-SERVICO, TAX-CPF=IN-CPF). Forcamos
        # COD-SERVICO=17 e SENHA numerica; o seeder marca TAX_TIPO=17 nas
        # linhas de roteiro pra chave composta casar.
        'map_moves': [('IN-CPF', 'COB_CPF')],
        'forcar': [('IN-CODE', 'RAUT'), ('IN-COD-SERVICO', '17'),
                   ('IN-SENHA-04', '0001')],
        'apos_perform': [
            # sinal achou/nao-achou da consulta TAXADS por CPF (0=achou taxa,
            # 1=nao achou) exposto como RESULT= observavel.
            (r'PERFORM 310-E-VERTAXA           THRU        310-S-VERTAXA\.',
             ['           DISPLAY "RESULT=" CH-NOTF']),
        ],
        # A ponte SQLite nao pagina FIND PRIOR/LAST (PDSQL_QRY devolve sempre
        # a mesma 1a linha); o 'GO 310-LOOP' apos o FIND PRIOR entao faz loop
        # infinito quando a taxa EXISTE. Como a consulta por (tipo,CPF) ja e'
        # data-dependent na 1a leitura, encerramos o laco: GO 310-LOOP ->
        # GO 310-S-VERTAXA (sai apos a 1a passada).
        'substituir': [
            (r'(?m)^           GO                              TO          310-LOOP\.',
             '      * INJECAO-ROTEIRO-INPUT: loop de FIND PRIOR (sem paginacao na ponte) encerrado\n'
             '           GO                              TO          310-S-VERTAXA.'),
        ],
    },
    # OGAA640D (EDUT/emissao de CRV): NAO habilitado para injecao data-dependent.
    # Motivo (avaliado): a consulta GEVER (10700-E-GEVER) fica varios niveis
    # dentro da logica da transacao EDUT (PERFORMada em 10451/11512, nao no
    # dispatch de topo), atras de mais portoes que os de OGAA018D; alem disso o
    # fonte e' grande e a compilacao com auto-inferidor leva ~124s (acima do
    # timeout tipico de teste). Custo/beneficio ruim vs OGAA018D/OGAA920D que
    # ja provam a consulta real data-dependent. Fica no comportamento honesto
    # "executa via runtime SQLite real, sem abortar".
}

# marca de injecao (idempotencia)
_MARCA = '      * INJECAO-ROTEIRO-INPUT (A-minimo)'
_RE_PERFORM_GET = re.compile(
    r'(?im)^(.*PERFORM\s+CONTAINER-GET\s+THRU\s+END-CONTAINER-GET.*)$')


# Legenda do RESULT= observavel injetado por programa (o que cada codigo
# significa em termos de negocio). Usada pela UI de testes/roteiro.
RESULT_LEGENDA = {
    'OGAA018D': {
        'campo': 'CH-NOT-GEVER (via consulta real GEVERDS por chassi)',
        'legenda': {
            '0': 'Ficha de emplacamento ENCONTRADA no GEVER para o chassi (consulta real ao banco)',
            '1': 'Ficha NAO encontrada no GEVER para o chassi (consulta real ao banco)',
        },
    },
    'OGAA920D': {
        'campo': 'CH-NOTF (via consulta real TAXADS por tipo+CPF)',
        'legenda': {
            '0': 'Taxa ENCONTRADA no TAXADS para o CPF (consulta real ao banco)',
            '1': 'Taxa NAO encontrada no TAXADS para o CPF (consulta real ao banco)',
        },
    },
}


# Campo de entrada REAL que cada programa configurado usa como CHAVE de
# consulta ao banco (env var + rotulo). Serve para o relatorio dizer com
# honestidade qual dado do roteiro foi de fato usado como chave - em vez do
# rotulo generico "chassi enviado tambem como placa". 'envvar' e a variavel de
# ambiente que o injetor le; 'rotulo' e o que mostrar; 'contexto' lista os
# outros dados do cenario que NAO sao chave deste programa (so' informativos).
ENTRADA_REAL = {
    'OGAA018D': {'envvar': 'COB_CHASSI', 'rotulo': 'Chassi (chave da consulta GEVERDS)',
                 'contexto': ['COB_CPF']},
    'OGAA920D': {'envvar': 'COB_CPF', 'rotulo': 'CPF (chave da consulta TAXADS)',
                 'contexto': []},
    # OGAA640D consulta GEVERDS por chassi; nao esta habilitado para resultado
    # data-dependent (ver comentario no CONFIG), mas a chave que ele consumiria
    # e o chassi - rotulo honesto.
    'OGAA640D': {'envvar': 'COB_CHASSI', 'rotulo': 'Chassi (consulta GEVERDS - execucao sem valor de negocio verificavel neste ambiente)',
                 'contexto': ['COB_CPF']},
}


def tem_config(nome_programa: str) -> bool:
    return nome_programa.upper() in CONFIG


def info_resultado(nome_programa: str) -> dict | None:
    """Retorna {campo, legenda} do RESULT observavel injetado, ou None."""
    return RESULT_LEGENDA.get(nome_programa.upper())


def info_entrada(nome_programa: str) -> dict | None:
    """Retorna {envvar, rotulo, contexto} da chave de entrada real, ou None."""
    return ENTRADA_REAL.get(nome_programa.upper())


def _campo_existe(campo: str, blob_upper: str) -> bool:
    """O campo esta declarado (nivel NN NOME) numa linha nao comentada?"""
    tok = re.escape(campo.upper())
    for ln in blob_upper.split('\n'):
        if len(ln) >= 7 and ln[6] in ('*', '/'):
            continue
        if re.search(r'\b\d{2}\s+' + tok + r'\b', ln):
            return True
    return False


def _blob_campos(processed_text: str, copy_dir: Path) -> str:
    """Fonte processado + todos os copybooks .cpy, em maiusculas, para checar
    a existencia de campos que vivem em copybooks (COFI02, header do container)
    e nao no fonte ainda-nao-expandido."""
    blob = processed_text
    try:
        for cpy in copy_dir.glob('*.cpy'):
            blob += '\n' + cpy.read_text(encoding='latin-1', errors='ignore')
    except Exception:
        pass
    return blob.upper()


def _linhas_injecao(nome_programa: str, blob_upper: str) -> list:
    cfg = CONFIG.get(nome_programa.upper())
    if not cfg:
        return []
    linhas = [_MARCA]
    for campo, envvar in cfg.get('map_moves', []):
        if _campo_existe(campo, blob_upper):
            linhas.append('           ACCEPT %s FROM ENVIRONMENT "%s"' % (campo, envvar))
    for campo, literal in cfg.get('forcar', []):
        if _campo_existe(campo, blob_upper):
            linhas.append('           MOVE "%s" TO %s' % (literal, campo))
    # so' vale a pena se pelo menos um MOVE/ACCEPT real foi gerado
    return linhas if len(linhas) > 1 else []


def injetar_no_processado(nome_programa: str, processed_path: Path,
                          copy_dir: Path) -> bool:
    """Injeta o bloco de entrada do roteiro logo apos o PERFORM CONTAINER-GET
    no fonte processado. Retorna True se injetou. Idempotente."""
    if not tem_config(nome_programa):
        return False
    try:
        texto = processed_path.read_text(encoding='latin-1', errors='ignore')
    except Exception:
        return False
    if _MARCA in texto:
        return True  # ja injetado
    blob = _blob_campos(texto, copy_dir)
    linhas = _linhas_injecao(nome_programa, blob)
    if not linhas:
        return False
    bloco = '\n'.join(linhas)

    def _repl(m):
        return m.group(1) + '\n' + bloco

    novo, n = _RE_PERFORM_GET.subn(_repl, texto, count=1)
    if n == 0:
        return False

    # injecoes 'apos_perform': neutralizam portoes de sessao/consistencia
    # (ex: habilitacao de terminal) inserindo COBOL logo apos um PERFORM
    # especifico, antes do teste de erro que pularia a transacao.
    cfg = CONFIG.get(nome_programa.upper(), {})
    for anchor_re, cobol_lines in cfg.get('apos_perform', []):
        rx = re.compile(r'(?im)^(.*' + anchor_re + r'.*)$')
        bloco_ap = _MARCA + '\n' + '\n'.join(cobol_lines)

        def _repl_ap(m, _b=bloco_ap):
            return m.group(1) + '\n' + _b

        novo, na = rx.subn(_repl_ap, novo, count=1)

    # substituicoes: trocam trechos ativos (ex: GO incondicional artefato de
    # conversao) por outra coisa (CONTINUE).
    for padrao, troca in cfg.get('substituir', []):
        novo, ns = re.subn(padrao, troca, novo, count=1)

    processed_path.write_text(novo, encoding='latin-1')
    return True
