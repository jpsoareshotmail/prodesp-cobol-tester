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

# Passos comuns do fluxo de primeiro emplacamento
_PASSOS_BASE = [
    {"ordem": 1, "titulo": "Verificar chassi na base fabril", "transacao": "901",
     "descricao": "O chassi deve existir na base fabril do Serpro e estar sem emplacamento na BIN/Serpro."},
    {"ordem": 2, "titulo": "Incluir taxa (cod. pagamento 06)", "transacao": "RAUT",
     "descricao": "Taxa enviada pela SEFAZ, recebida via RAUT (window WDGAA35) ou batch GAA/B100/DB. NAO se aplica a categoria oficial."},
    {"ordem": 3, "titulo": "Consultar taxa", "transacao": "TXUT",
     "descricao": "Confirma a taxa de codigo 06 vinculada ao CPF."},
    {"ordem": 4, "titulo": "Criar ficha de emplacamento", "transacao": None,
     "descricao": "Cria-se a ficha no eCRV, escolhe placa gratuita, preenche e ENVIAR gera a ficha no mainframe."},
    {"ordem": 5, "titulo": "Consultar ficha", "transacao": "PGER",
     "descricao": "Consulta a ficha gerada no mainframe."},
    {"ordem": 6, "titulo": "Aprovar ficha (eCRV)", "transacao": "PGER",
     "descricao": "Aprova a ficha (SALVAR) e altera a situacao de 1 para 5."},
    {"ordem": 7, "titulo": "Processar (DHAB)", "transacao": "DHAB",
     "descricao": "Executa DHAB (uma vez por dia) para iniciar o processamento do emplacamento."},
    {"ordem": 8, "titulo": "Autorizacao de estampagem", "transacao": "PEPM",
     "descricao": "Placa cadastrada no Detran (PEPM) e na base fabril (PTRE); opcoes de autorizacao de estampagem."},
    {"ordem": 9, "titulo": "Emissao de CRV", "transacao": "EDUT",
     "descricao": "Base ampliada fica com pendencia de emissao de CRV; executa EDUT."},
    {"ordem": 10, "titulo": "Consultar cadastro da placa", "transacao": "CDAV",
     "descricao": "Verifica cadastro: PEPM (estadual), BIN, PTRE (fabril), CDAV (ampliada)."},
    {"ordem": 11, "titulo": "Cancelar estampagem (fallback)", "transacao": "CEST",
     "descricao": "Na ausencia de parceria com o sistema EMPLACA, consulta PEST e cancela via CEST."},
]


def _passos_oficial():
    """Fluxo do orgao oficial: sem taxa 06, com verificacao de CNPJ oficial."""
    passos = [p for p in _PASSOS_BASE if p["ordem"] not in (2, 3)]  # remove taxa
    # insere verificacao de CNPJ oficial antes do processamento
    passos.insert(4, {"ordem": 6.5, "titulo": "Verificar CNPJ oficial", "transacao": "PJOF",
                      "descricao": "Categoria oficial exige o CNPJ no cadastro de CNPJ oficial (PJOF). Se nao existir, deve ser inserido."})
    return passos


ROTEIROS = [
    {
        "id": "capital",
        "nome": "Primeiro Emplacamento - Capital",
        "cenario": "Capital",
        "categoria": "Particular",
        "dados_teste": {"chassi": "9C2GAA1SNSP772009", "cpf": "09758787861"},
        "passos": _PASSOS_BASE,
    },
    {
        "id": "interior_litoral",
        "nome": "Primeiro Emplacamento - Interior/Litoral",
        "cenario": "Interior/Litoral",
        "categoria": "Particular",
        "dados_teste": {"chassi": "9BMGAA1SNSP772016", "cpf": "81742145850"},
        "passos": _PASSOS_BASE,
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
