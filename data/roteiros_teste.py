"""
Roteiros de teste funcional do processo de Primeiro Emplacamento.

Extraidos dos documentos em 'Roteiros de Teste/*.docx' e estruturados para
uso no dashboard. Cada roteiro descreve um cenario (capital, interior/litoral,
orgao oficial) com seus dados de teste (chassi, CPF/CNPJ) e o passo a passo
com as transacoes do mainframe envolvidas.
"""

# Transacoes citadas nos roteiros -> descricao e programa COBOL relacionado (quando conhecido)
TRANSACOES = {
    "901":  {"descricao": "Consulta veiculo por chassi na BIN/Serpro", "sistema": "BIN"},
    "RAUT": {"descricao": "Inclusao de taxa (recebimento SEFAZ)", "window": "WDGAA35"},
    "GAA/B100/DB": {"descricao": "Batch de contingencia - recebimento de taxa", "programa": "PGAA100D", "fonte": "PF-GAA-B100-DB"},
    "TXUT": {"descricao": "Consulta de taxa"},
    "PGER": {"descricao": "Consulta/situacao da ficha no mainframe"},
    "DHAB": {"descricao": "Processamento diario (habilitacao)"},
    "PEPM": {"descricao": "Cadastro da placa na base estadual (Detran)"},
    "PTRE": {"descricao": "Base fabril da BIN"},
    "EDUT": {"descricao": "Emissao de CRV"},
    "CDAV": {"descricao": "Consulta da base ampliada da BIN"},
    "PJOF": {"descricao": "Cadastro de CNPJ oficial"},
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
    """Fluxo do orgao oficial: sem taxa 06, com verificacao de CNPJ oficial (PJOF)."""
    # remove os passos de taxa (2 e 3) e renumera de forma limpa
    base = [p for p in _PASSOS_PARTICULAR if p["ordem"] not in (2, 3)]
    passo_cnpj = {"titulo": "Verificar CNPJ oficial", "camada": "Mainframe", "transacao": "PJOF",
                  "descricao": "Categoria oficial exige o CNPJ no cadastro de CNPJ oficial (PJOF); se nao existir, deve ser inserido.",
                  "resultado_esperado": "CNPJ oficial encontrado (ou inserido, se ausente)."}
    # inserir o passo de CNPJ logo apos consultar chassi
    ordenados = base[:1] + [passo_cnpj] + base[1:]
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
