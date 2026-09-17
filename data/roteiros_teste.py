"""
Roteiros de teste funcional do processo de Primeiro Emplacamento.

Extraidos dos documentos em 'Roteiros de Teste/*.docx' e estruturados para
uso no dashboard. Cada roteiro descreve um cenario (capital, interior/litoral,
orgao oficial) com seus dados de teste (chassi, CPF/CNPJ) e o passo a passo
com as transacoes do mainframe envolvidas.
"""

# Ambiente observado nos prints dos roteiros (Unisys ClearPath MCP via Web Enabler)
AMBIENTE = {
    "host": "HNPRDSP06",
    "ip": "10.200.206.132",
    "window": "WDMCS/1",
    "plataforma": "Unisys ClearPath MCP (Web Enabler)",
}

# Transacoes citadas nos roteiros -> descricao, tela real (dos prints) e programa COBOL relacionado.
#
# Associacao tela->programa feita cruzando os prints de tela reais (frontend/
# static/roteiros/*/*.png) com comentarios de cabecalho e o literal da
# transacao gravado no codigo (ex: MOVE "CAV2" TO TAX-TRANSACAO) - nao e'
# uma inferencia de nome, e' o proprio fonte se identificando. "programa"/
# "fonte" so' aparecem quando essa evidencia direta foi encontrada; varias
# transacoes (901, TXUT, PTRE, PEST, CEST) sao de sistemas externos (BIN/
# Serpro) ou telas cujo programa de fato nao esta entre os 42 fontes
# entregues - ficam sem "programa" de proposito, nao e' lacuna de busca.
TRANSACOES = {
    "901":  {"descricao": "Consulta veiculo por chassi na BIN/Serpro", "sistema": "BIN",
             "tela": "PER1 - Pesquisa de veiculos cadastrados no sistema RENAVAM"},
    "RAUT": {"descricao": "Inclusao de taxa (recebimento SEFAZ)", "window": "WDGAA35",
             "programa": "OGAA920D", "fonte": "PF-GAA-T920-DB"},
    "GAA/B100/DB": {"descricao": "Batch de contingencia - recebimento de taxa", "programa": "PGAA100D", "fonte": "PF-GAA-B100-DB"},
    "TXUT": {"descricao": "Consulta de taxa (Cadastro de Certificados Emitidos)",
             "tela": "TXUT - Pesquisa de taxas por CPF/CNPJ (COD.SERV 06, situacao 0-Aguarda Uso)"},
    "CAV1": {"descricao": "Verificacao de bloqueios/debitos/incompatibilidades no cadastro (opcao 1)",
             "tela": "CAV1 - Verificacao de bloqueios, debitos e incompatibilidades / Primeiro Emplacamento (veiculo zero)",
             "programa": "OGAA013D", "fonte": "PF-GAA-T013-DB"},
    "CAFI": {"descricao": "Acesso a ficha de emplacamento por numero+ano (comando CAFI+ficha,ano)",
             "tela": "PGE4/GEVER - status do registro (acessado digitando CAFI+NRO-FICHA+ANO-FICHA)",
             "programa": "OGEV005D", "fonte": "PF-GEV-T005-DB"},
    "PGER": {"descricao": "Consulta/situacao da ficha (GEVER - situacao de registro em GEVERDS); "
             "acessada na pratica pelo comando CAFI (ver transacao CAFI)",
             "tela": "PGE4/GEVER - status do registro (STATUS REG 01->05)"},
    "DHAB": {"descricao": "Processamento diario (habilitacao) - nao e' um programa proprio: e' uma "
             "mensagem (MOVE \"DHAB\" TO MENSCODE) enviada por OGAA013D/OGAA018D/OGAA640D"},
    "PEPM": {"descricao": "Cadastro da placa na base estadual (Detran)",
             "tela": "CAV2 - Cadastro de Certificados Emitidos / Primeiro Emplacamento",
             "programa": "OGAA018D", "fonte": "PF-GAA-T018-DB"},
    "PTRE": {"descricao": "Base fabril da BIN", "tela": "PTRE"},
    "EDUT": {"descricao": "Emissao do Documento Unico de Transito (CRV)",
             "tela": "DUT1 - Emissao do documento unico de transito (1a via)",
             "programa": "OGAA640D", "fonte": "PF-GAA-T640-DB"},
    "CDAV": {"descricao": "Consulta dados ampliados do veiculo na RENAVAM (TR.227); dado alimentado "
             "por OGAA255D (transacoes internas AUMI/AUCA), mas a tela de consulta CDAV em si "
             "nao esta entre os 42 fontes entregues",
             "tela": "CDAV - IND.CRV ELETR=SIM, numero CRV gerado"},
    "PJOF": {"descricao": "Cadastro de CNPJ oficial - a tela de manutencao (PJO1/PJO2) nao esta entre "
             "os 42 fontes; OGAA013D/OGAA018D/OGAA792D/OGEV050D apenas leem CNPJOFICIALDS para validar",
             "tela": "PJO1 (menu: 1-Inclusao, 2-Exclusao, 3-Pesquisa) / PJO2 (inclusao: CNPJ, categoria M/E/U, nome, atividade)"},
    "PESQ10": {"descricao": "Pesquisa de veiculos de uso exclusivo do Detran - nao esta entre os 42 fontes entregues",
               "tela": "PESQ10 - Cadastro de veiculos, pesquisa de uso exclusivo do Detran"},
    "PEST": {"descricao": "Consulta de estampagem"},
    "CEST": {"descricao": "Cancelamento de estampagem"},
}

# Passos do fluxo particular (Capital / Interior-Litoral).
# Cada passo: camada (Externo/eCRV/Mainframe), transacao e resultado esperado.
_PASSOS_PARTICULAR = [
    {"ordem": 1, "titulo": "Consultar chassi na BIN/Serpro", "camada": "Externo (BIN)", "transacao": "901",
     "descricao": "O chassi deve existir na base fabril do Serpro.",
     "resultado_esperado": "Chassi encontrado e retorna 'sem emplacamento' na BIN/Serpro."},
    {"ordem": 2, "titulo": "Incluir taxa (cod. pagamento 06)", "camada": "Mainframe", "transacao": "RAUT",
     "descricao": "Taxa enviada pela SEFAZ, recebida via RAUT (window WDGAA35) ou batch GAA/B100/DB.",
     "resultado_esperado": "Taxa codigo 06 registrada e vinculada ao CPF."},
    {"ordem": 3, "titulo": "Consultar taxa", "camada": "Mainframe", "transacao": "TXUT",
     "descricao": "Confirma a taxa de codigo 06 vinculada ao CPF.",
     "resultado_esperado": "TXUT exibe a taxa 06 do CPF."},
    {"ordem": 4, "titulo": "Criar ficha de emplacamento", "camada": "eCRV", "transacao": None,
     "descricao": "No eCRV: escolhe placa gratuita, preenche a ficha e clica ENVIAR.",
     "resultado_esperado": "Ficha gerada no mainframe com situacao = 1."},
    {"ordem": 5, "titulo": "Consultar ficha", "camada": "Mainframe", "transacao": "PGER",
     "descricao": "Consulta a ficha gerada no mainframe.",
     "resultado_esperado": "Ficha existe com situacao = 1."},
    {"ordem": 6, "titulo": "Aprovar ficha (SALVAR)", "camada": "eCRV", "transacao": None,
     "descricao": "No eCRV, a ficha passa por avaliacao e clica-se SALVAR para aprovar.",
     "resultado_esperado": "Aprovacao da ficha registrada."},
    {"ordem": 7, "titulo": "Confirmar mudanca de situacao", "camada": "Mainframe", "transacao": "PGER",
     "descricao": "Verifica a situacao da ficha apos a aprovacao.",
     "resultado_esperado": "Situacao da ficha muda de 1 para 5."},
    {"ordem": 8, "titulo": "Processar (DHAB)", "camada": "Mainframe", "transacao": "DHAB",
     "descricao": "Executa DHAB (uma vez por dia) para iniciar o processamento.",
     "resultado_esperado": "Processamento do primeiro emplacamento iniciado."},
    {"ordem": 9, "titulo": "Verificar placa e estampagem", "camada": "Mainframe", "transacao": "PEPM",
     "descricao": "Placa cadastrada no Detran (PEPM) e base fabril (PTRE); opcoes de estampagem.",
     "resultado_esperado": "Placa presente em PEPM e PTRE; opcoes de autorizacao de estampagem exibidas."},
    {"ordem": 10, "titulo": "Emissao de CRV", "camada": "Mainframe", "transacao": "EDUT",
     "descricao": "Base ampliada fica com pendencia de emissao de CRV; executa EDUT.",
     "resultado_esperado": "Pendencia eliminada e CRV emitido."},
    {"ordem": 11, "titulo": "Consultar cadastro completo", "camada": "Mainframe", "transacao": "CDAV",
     "descricao": "Verifica o cadastro nas bases: PEPM (estadual), BIN, PTRE (fabril), CDAV (ampliada).",
     "resultado_esperado": "Placa presente e consistente nas quatro bases; emplacamento concluido."},
    {"ordem": 12, "titulo": "(Excecao) Cancelar estampagem", "camada": "Externo/Mainframe", "transacao": "CEST",
     "descricao": "Na ausencia de parceria com o sistema EMPLACA, consulta PEST e cancela via CEST.",
     "resultado_esperado": "Solicitacao de autorizacao de estampagem cancelada."},
]


def _passos_oficial():
    """Fluxo do orgao oficial: sem taxa 06, com verificacao de CNPJ oficial (PJOF).

    Posicao do passo de CNPJ validada contra o texto real do documento
    'PrimeiroEmplacamento_orgao_oficial.docx': a verificacao/inclusao do
    CNPJ oficial (PJOF) acontece DEPOIS de "Processar (DHAB)" e ANTES de
    "Inicio do processamento do primeiro emplacamento" - nao logo apos
    consultar o chassi, como uma versao anterior deste arquivo tinha.
    """
    # remove os passos de taxa (2 e 3)
    base = [p for p in _PASSOS_PARTICULAR if p["ordem"] not in (2, 3)]
    passo_cnpj = {"titulo": "Verificar/incluir CNPJ oficial", "camada": "Mainframe", "transacao": "PJOF",
                  "descricao": "PJO1 opcao 3 pesquisa o CNPJ; se retornar 'CNPJ NAO CADASTRADO', usa-se PJO1 opcao 1 -> PJO2 para incluir (categoria M/E/U, nome do orgao, atividade economica).",
                  "resultado_esperado": "CNPJ oficial presente no cadastro (pesquisa OK) ou incluido com sucesso via PJO2."}
    idx_dhab = next(i for i, p in enumerate(base) if p["titulo"].startswith("Processar (DHAB)"))
    ordenados = base[:idx_dhab + 1] + [passo_cnpj] + base[idx_dhab + 1:]
    # renumerar 1..N
    for i, p in enumerate(ordenados, start=1):
        p = dict(p)
        p["ordem"] = i
        ordenados[i - 1] = p
    return ordenados


ROTEIROS = [
    {
        "id": "capital",
        "nome": "Primeiro Emplacamento - Capital",
        "cenario": "Capital",
        "categoria": "Particular",
        "dados_teste": {"chassi": "9C2GAA1SNSP772009", "cpf": "09758787861"},
        "passos": _PASSOS_PARTICULAR,
    },
    {
        "id": "interior_litoral",
        "nome": "Primeiro Emplacamento - Interior/Litoral",
        "cenario": "Interior/Litoral",
        "categoria": "Particular",
        "dados_teste": {"chassi": "9BMGAA1SNSP772016", "cpf": "81742145850"},
        "passos": _PASSOS_PARTICULAR,
    },
    {
        "id": "orgao_oficial",
        "nome": "Primeiro Emplacamento - Orgao Oficial",
        "cenario": "Orgao Oficial",
        "categoria": "Oficial",
        "dados_teste": {"chassi": "9C2GAA1SNSP772010", "cnpj": "08518623000162"},
        "passos": _passos_oficial(),
    },
]


def get_roteiros() -> list:
    """Retorna os roteiros com as transacoes enriquecidas."""
    return ROTEIROS


def get_transacoes() -> dict:
    return TRANSACOES
