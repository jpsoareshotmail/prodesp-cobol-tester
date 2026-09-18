"""
Cenarios de teste ficticios para programas parametrizados sem DB2 real.

Sem banco de verdade, um FETCH neutralizado sempre simula "nao encontrado"
(ver sql_preprocessor.py) - todo teste dá o mesmo resultado generico (ex:
"0 = nada consta"), mesmo para programas cujo fonte documenta varios
codigos de resultado possiveis (ex: FGAA012D: 0-9, 88).

Este modulo mapeia, POR PROGRAMA, quais cursores/tabelas simulam qual
"cenario" quando o usuario escolhe um na tela de testes (variavel de
ambiente COB_CENARIO). Quando um cenario e' escolhido, o stub do FETCH
daquele cursor especifico passa a simular "OK" e preenche os campos reais
(sem sufixo -X - as rotinas *-DB2DMS que fariam essa copia estao vazias
neste ambiente, entao os campos "-X" do FETCH nao teriam efeito nenhum
sozinhos) com os valores do cenario; os DEMAIS cursores do mesmo programa
continuam simulando NOTFOUND normalmente. Como so' um cursor "acha" por
vez, as regras de prioridade por data entre tabelas concorrentes (quando
existem no fonte original) nunca chegam a ser exercitadas - o resultado
final e' calculado pela logica real do programa a partir do "registro"
fabricado, nao fabricado diretamente.

Levantado por investigacao linha-a-linha dos 7 programas parametrizados
com FETCH (ver commits desta sessao) - nao e' inferencia, e' o que o
fonte de cada um realmente faz com esses campos.

FGAA050D fica de fora: seu AX-L050-SIT e' hoje uma constante 0 (regra de
negocio "TODO USU APTO A SERVICO DE QQ LUGAR", 20/04/21) independente do
FETCH achar ou nao - nao ha cenario nenhum pra simular sem editar logica
de negocio de verdade (fora do escopo de um fixture de teste).
"""

CENARIOS = {
    # AX-GAA-RET: 0=nada consta / 1-9=tipo de crime (QUEIXADS) / 88=alerta (ALERTADS)
    'FGAA012D': [
        {'cursor': 'QXACHASS', 'cenarios': {str(n): {'QXA-TIPO-DECL': '%02d' % n} for n in range(1, 10)}},
        {'cursor': 'QXAPLASS', 'cenarios': {str(n): {'QXA-TIPO-DECL': '%02d' % n} for n in range(1, 10)}},
        {'cursor': 'ALECHASS', 'cenarios': {'88': {}}},
        {'cursor': 'ALEPLASS', 'cenarios': {'88': {}}},
    ],
    # Mesma legenda/campos que FGAA012D (confirmado: mesmos cursores QXACHASS/
    # QXAPLASS/ALECHASS/ALEPLASS, mesmo campo QXA-TIPO-DECL PIC X(006)).
    'FGAA032D': [
        {'cursor': 'QXACHASS', 'cenarios': {str(n): {'QXA-TIPO-DECL': '%02d' % n} for n in range(1, 10)}},
        {'cursor': 'QXAPLASS', 'cenarios': {str(n): {'QXA-TIPO-DECL': '%02d' % n} for n in range(1, 10)}},
        {'cursor': 'ALECHASS', 'cenarios': {'88': {}}},
        {'cursor': 'ALEPLASS', 'cenarios': {'88': {}}},
    ],
    # AX-RL115-RET: 0=nao encontrado / 1=encontrado (obito registrado)
    'FGAA115D': [
        {'cursor': 'OBICPFSE', 'cenarios': {'1': {'OBI-CPF': '09758787861'}}},
    ],
    # AX-RET-BLOQ(1..6): legenda de tipo de bloqueio (01-54, ver comentario no
    # fonte). Oferece um subconjunto representativo dos 3 grupos de
    # classificacao (Jud/Adm/Trib) usados no codigo, mais alguns tipos que so'
    # aparecem no comentario. BLO-DT-INCLUSAO=20200101 (recente) evita a regra
    # "tipo 02 antes de 29/07/1996 vira 31" mudar o codigo sem querer.
    # 'zerar': o programa so' aceita um "achado" em AX-RET-BLOQ(N) quando o
    # slot ainda esta' = ZEROS (ver comentario em sql_preprocessor._stub_sql)
    # - sem isso o resultado simulado nunca chega no campo de saida real.
    'FGAT006D': [
        {'cursor': 'BLOCHASSE-FNDNXAT',
         'zerar': ['AX-RET-BLOQ(1)', 'AX-RET-BLOQ(2)', 'AX-RET-BLOQ(3)',
                    'AX-RET-BLOQ(4)', 'AX-RET-BLOQ(5)', 'AX-RET-BLOQ(6)'],
         'cenarios': {
            str(n): {'BLO-TIP-BLOQ': str(n), 'BLO-CHASSIS': '9C2GAA1SNSP772009    ',
                     'BLO-MUNICIPIO': '00000', 'BLO-PLACA-MERC': 'ABC1D23   ',
                     'BLO-DT-INCLUSAO': '20200101'}
            for n in [1, 2, 4, 7, 11, 14, 31, 35, 40, 41]
        }},
    ],
    # AX-RETL030-RESTRBIN(1..4): mesma legenda/campo BLO-TIP-BLOQ de FGAT006D,
    # sem a regra de data (BLO-DT-INCLUSAO nao existe neste programa).
    'FGAT030D': [
        {'cursor': 'BLOCHASSE-FNDPRAT',
         'zerar': ['AX-RETL030-RESTRBIN(1)', 'AX-RETL030-RESTRBIN(2)',
                    'AX-RETL030-RESTRBIN(3)', 'AX-RETL030-RESTRBIN(4)'],
         'cenarios': {
            str(n): {'BLO-TIP-BLOQ': str(n), 'BLO-PLACA-MERC': 'ABC1D23   ',
                     'BLO-MUNICIPIO': '00000'}
            for n in [1, 2, 4, 7, 11, 14, 31, 35, 40, 41]
        }},
    ],
    # AX-RCV-FLAG: 0=nao encontrado OU encontrado-sem-documento / 1=encontrado
    # com comunicacao de venda valida (CVV-DT-DOCTS > 0).
    'FGEV006D': [
        {'cursor': 'CVVCHASSISE', 'cenarios': {
            '1': {'CVV-DT-DOCTS': '20250101', 'CVV-PLACA-MERC': 'ABC1D23   ',
                  'CVV-CHASSI': '9C2GAA1SNSP772009    ', 'CVV-MUNICIPIO': '00000'},
            '2': {'CVV-DT-DOCTS': '0'},
        }},
    ],
}

# Rotulos exibidos na tela (codigo -> descricao). So' cobre os codigos que
# realmente aparecem em algum programa acima.
ROTULOS = {
    ('FGAA012D', '1'): 'Roubo', ('FGAA012D', '2'): 'Furto',
    ('FGAA012D', '3'): 'Apropriacao indebita', ('FGAA012D', '4'): 'Estelionato',
    ('FGAA012D', '5'): 'Veiculo e pessoa desaparecida', ('FGAA012D', '6'): 'Extorsao',
    ('FGAA012D', '7'): 'Concussao', ('FGAA012D', '8'): 'Peculato',
    ('FGAA012D', '9'): 'Outros crimes', ('FGAA012D', '88'): 'Alerta de furto/roubo',
    ('FGAA115D', '1'): 'CPF encontrado (obito registrado)',
    ('FGAT006D', '1'): 'Judicial', ('FGAT006D', '2'): 'Falta de transferencia',
    ('FGAT006D', '4'): 'Veiculo importado usado', ('FGAT006D', '7'): 'Pendencia judicial/administrativa',
    ('FGAT006D', '11'): 'Acao judicial', ('FGAT006D', '14'): 'Veiculo sinistrado',
    ('FGAT006D', '31'): 'Veiculo bloqueado pelo Detran', ('FGAT006D', '35'): 'Judicial - libera licenciamento',
    ('FGAT006D', '40'): 'Veiculo sinistrado (media monta)', ('FGAT006D', '41'): 'Veiculo sinistrado (grande monta)',
    ('FGEV006D', '1'): 'Encontrado - comunicacao de venda valida',
    ('FGEV006D', '2'): 'Encontrado - sem documento (nao conta)',
}
# FGAA032D e FGAT030D compartilham a mesma legenda de FGAA012D/FGAT006D
for _n in range(1, 10):
    ROTULOS[('FGAA032D', str(_n))] = ROTULOS[('FGAA012D', str(_n))]
ROTULOS[('FGAA032D', '88')] = ROTULOS[('FGAA012D', '88')]
for _n in [1, 2, 4, 7, 11, 14, 31, 35, 40, 41]:
    ROTULOS[('FGAT030D', str(_n))] = ROTULOS[('FGAT006D', str(_n))]


def cenarios_disponiveis(nome_programa: str) -> list:
    """Lista [{codigo, rotulo}] dos cenarios de teste disponiveis para o
    programa, na ordem em que devem aparecer na tela (0/generico primeiro,
    coletado de todas as regras de cursor do programa, sem duplicar)."""
    regras = CENARIOS.get(nome_programa)
    if not regras:
        return []
    vistos = []
    for regra in regras:
        for codigo in regra['cenarios']:
            if codigo not in vistos:
                vistos.append(codigo)
    def chave_ordenacao(c):
        try:
            return (0, int(c))
        except ValueError:
            return (1, c)
    vistos.sort(key=chave_ordenacao)
    return [{'codigo': c, 'rotulo': ROTULOS.get((nome_programa, c), c)} for c in vistos]
