#!/usr/bin/env python3
"""
Dados Mockados para Testes Customizados
Fornece dados de exemplo para cada programa COBOL
"""

MOCK_DATA = {
    # Validador de Placas
    "PF-GAA-L004": {
        "tipo": "placa",
        "descricao": "Validador de Placas",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "placeholder": "Digite a placa (ex: AAA0A00)",
                "valor": "AAA0A00",
                "maxlength": 10
            }
        ],
        "exemplos": [
            {"placa": "AAA0A00", "descricao": "Mercosul - São Paulo"},
            {"placa": "AB12C34", "descricao": "2 letras - Carros"},
            {"placa": "SP1234", "descricao": "Placa Antiga - SP"},
            {"placa": "ABC-1234", "descricao": "Com caractere especial"},
            {"placa": "", "descricao": "Vazia"},
        ]
    },

    # Programas GEV (Gestão Empadronização Veicular)
    "PF-GEV-L006-DB": {
        "tipo": "veiculo",
        "descricao": "Gestão Empadronização Veicular",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa do Veículo",
                "tipo": "texto",
                "placeholder": "Ex: AAA0A00",
                "valor": "AAA0A00",
                "maxlength": 10
            },
            {
                "nome": "ano",
                "label": "Ano de Fabricação",
                "tipo": "numero",
                "placeholder": "2020",
                "valor": "2020",
                "min": "1980",
                "max": "2026"
            },
            {
                "nome": "marca",
                "label": "Marca do Veículo",
                "tipo": "texto",
                "placeholder": "Ex: Toyota",
                "valor": "Toyota",
                "maxlength": 50
            }
        ],
        "exemplos": [
            {
                "placa": "AAA0A00",
                "ano": "2020",
                "marca": "Toyota",
                "descricao": "Veículo Mercosul"
            },
            {
                "placa": "SP1234",
                "ano": "2010",
                "marca": "Volkswagen",
                "descricao": "Veículo Antigo"
            }
        ]
    },

    "PF-GEV-T005-DB": {
        "tipo": "documento",
        "descricao": "Tabela de Documentos",
        "campos": [
            {
                "nome": "numero",
                "label": "Número do Documento",
                "tipo": "texto",
                "placeholder": "123456789",
                "valor": "123456789",
                "maxlength": 20
            },
            {
                "nome": "tipo",
                "label": "Tipo de Documento",
                "tipo": "select",
                "valor": "RENAVAM",
                "opcoes": [
                    {"valor": "RENAVAM", "label": "RENAVAM"},
                    {"valor": "CRVA", "label": "CRVA"},
                    {"valor": "CRLV", "label": "CRLV"}
                ]
            }
        ],
        "exemplos": [
            {
                "numero": "123456789",
                "tipo": "RENAVAM",
                "descricao": "RENAVAM válido"
            },
            {
                "numero": "987654321",
                "tipo": "CRVA",
                "descricao": "CRVA válido"
            }
        ]
    },

    # Programas GAT (Gestão Autoridades)
    "PF-GAT-L006-DB": {
        "tipo": "autoridade",
        "descricao": "Gestão de Autoridades",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código da Autoridade",
                "tipo": "numero",
                "placeholder": "001",
                "valor": "001",
                "min": "001",
                "max": "999"
            },
            {
                "nome": "nome",
                "label": "Nome da Autoridade",
                "tipo": "texto",
                "placeholder": "Ex: DETRAN SP",
                "valor": "DETRAN SP",
                "maxlength": 100
            },
            {
                "nome": "uf",
                "label": "UF",
                "tipo": "select",
                "valor": "SP",
                "opcoes": [
                    {"valor": "SP", "label": "São Paulo"},
                    {"valor": "RJ", "label": "Rio de Janeiro"},
                    {"valor": "MG", "label": "Minas Gerais"},
                    {"valor": "BA", "label": "Bahia"},
                    {"valor": "RS", "label": "Rio Grande do Sul"}
                ]
            }
        ],
        "exemplos": [
            {
                "codigo": "001",
                "nome": "DETRAN SP",
                "uf": "SP",
                "descricao": "DETRAN São Paulo"
            },
            {
                "codigo": "002",
                "nome": "DETRAN RJ",
                "uf": "RJ",
                "descricao": "DETRAN Rio de Janeiro"
            }
        ]
    },

    "PF-GAT-T030-DB": {
        "tipo": "penalidade",
        "descricao": "Tabela de Penalidades",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código da Infração",
                "tipo": "numero",
                "placeholder": "0001",
                "valor": "0001",
                "min": "0001",
                "max": "9999"
            },
            {
                "nome": "descricao",
                "label": "Descrição",
                "tipo": "texto",
                "placeholder": "Ex: Estacionamento proibido",
                "valor": "Estacionamento proibido",
                "maxlength": 200
            },
            {
                "nome": "pontos",
                "label": "Pontos de Penalidade",
                "tipo": "numero",
                "placeholder": "3",
                "valor": "3",
                "min": "0",
                "max": "20"
            }
        ],
        "exemplos": [
            {
                "codigo": "0001",
                "descricao": "Estacionamento proibido",
                "pontos": "3",
                "descricao_ex": "Infração de estacionamento"
            },
            {
                "codigo": "0002",
                "descricao": "Dirigir sem habilitação",
                "pontos": "20",
                "descricao_ex": "Infração grave"
            }
        ]
    },

    # Padrão para programas sem dados específicos
    "DEFAULT": {
        "tipo": "generico",
        "descricao": "Programa COBOL Genérico",
        "campos": [
            {
                "nome": "entrada",
                "label": "Dados de Entrada",
                "tipo": "textarea",
                "placeholder": "Digite os dados de entrada",
                "valor": "",
                "rows": 5
            }
        ],
        "exemplos": []
    }
}


def get_mock_data(programa_nome):
    """Retorna dados mockados para um programa"""
    return MOCK_DATA.get(programa_nome, MOCK_DATA["DEFAULT"])


def get_todos_programas_com_dados():
    """Retorna lista de programas que têm dados mockados"""
    return list(MOCK_DATA.keys())


def validar_entrada(programa_nome, dados):
    """Valida dados de entrada para um programa"""
    mock = get_mock_data(programa_nome)
    erros = []

    for campo in mock["campos"]:
        nome_campo = campo["nome"]
        tipo_campo = campo["tipo"]

        if nome_campo not in dados:
            erros.append(f"Campo obrigatório: {campo['label']}")
            continue

        valor = dados[nome_campo]

        # Validações básicas
        if tipo_campo == "numero":
            try:
                int(valor)
            except ValueError:
                erros.append(f"{campo['label']} deve ser um número")

        if tipo_campo in ["texto", "numero"]:
            if "maxlength" in campo and len(str(valor)) > int(campo["maxlength"]):
                erros.append(f"{campo['label']} excede {campo['maxlength']} caracteres")

    return {"valido": len(erros) == 0, "erros": erros}
