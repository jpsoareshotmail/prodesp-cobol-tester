#!/usr/bin/env python3
"""
Dados Mockados Expandidos para Todos os 42 Programas COBOL
Fornece dados de entrada realistas e exemplos para cada programa
"""

MOCK_DATA_EXPANDED = {
    # ==================== GAA - Gestão Arquivo Automotivo ====================

    "PF-GAA-L004": {
        "tipo": "validacao_placa",
        "descricao": "Validador de Placas Veiculares",
        "objetivo": "Verifica se a placa está no formato permitido (Mercosul, Antiga, 2 letras). Retorna código indicando o tipo de placa identificado.",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa do Veículo",
                "tipo": "texto",
                "placeholder": "AAA0A00",
                "valor": "AAA0A00",
                "maxlength": 10
            }
        ],
        "exemplos": [
            {"placa": "AAA0A00", "descricao": "Mercosul - São Paulo"},
            {"placa": "AB12C34", "descricao": "2 letras - Carros"},
            {"placa": "SP1234", "descricao": "Placa Antiga - SP"},
            {"placa": "ABC-1234", "descricao": "Com caractere especial"},
            {"placa": "", "descricao": "Vazia"}
        ]
    },

    "PF-GAA-L005": {
        "tipo": "consulta_veiculo",
        "descricao": "Consulta Dados de Veículo",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            },
            {
                "nome": "documento",
                "label": "Documento RENAVAM",
                "tipo": "numero",
                "valor": "1234567890",
                "maxlength": 11
            }
        ],
        "exemplos": [
            {"placa": "AAA0A00", "documento": "1234567890", "descricao": "Veículo Mercosul"},
            {"placa": "SP1234", "documento": "0987654321", "descricao": "Veículo Antigo"}
        ]
    },

    "PF-GAA-L007": {
        "tipo": "validacao_documento",
        "descricao": "Validação de Documentação",
        "campos": [
            {
                "nome": "renavam",
                "label": "RENAVAM",
                "tipo": "numero",
                "valor": "1234567890",
                "maxlength": 11
            },
            {
                "nome": "crva",
                "label": "CRVA",
                "tipo": "numero",
                "valor": "0000000001",
                "maxlength": 10
            }
        ],
        "exemplos": [
            {"renavam": "1234567890", "crva": "0000000001", "descricao": "Documentos válidos"},
            {"renavam": "0000000000", "crva": "0000000000", "descricao": "Documentos inválidos"}
        ]
    },

    "PF-GAA-B100-DB": {
        "tipo": "banco_dados",
        "descricao": "Banco de Dados - Veículos",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            }
        ],
        "exemplos": [
            {"placa": "AAA0A00", "descricao": "Consulta banco"},
            {"placa": "ZZZ9Z99", "descricao": "Último registro"}
        ]
    },

    "PF-GAA-L012-DB": {
        "tipo": "emissao_documento",
        "descricao": "Emissão de Documentos",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            },
            {
                "nome": "tipo_doc",
                "label": "Tipo de Documento",
                "tipo": "select",
                "valor": "CRLV",
                "opcoes": [
                    {"valor": "CRLV", "label": "Certificado de Registro e Licenciamento"},
                    {"valor": "CRV", "label": "Certificado de Registro"},
                    {"valor": "DUT", "label": "Documento Único de Trânsito"}
                ]
            }
        ],
        "exemplos": [
            {"placa": "AAA0A00", "tipo_doc": "CRLV", "descricao": "CRLV 2026"},
            {"placa": "SP1234", "tipo_doc": "DUT", "descricao": "DUT antigo"}
        ]
    },

    "PF-GAA-L015": {
        "tipo": "transferencia",
        "descricao": "Processamento de Transferência",
        "campos": [
            {
                "nome": "placa_origem",
                "label": "Placa Origem",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            },
            {
                "nome": "placa_destino",
                "label": "Placa Destino",
                "tipo": "texto",
                "valor": "BBB0B00",
                "maxlength": 10
            }
        ],
        "exemplos": [
            {"placa_origem": "AAA0A00", "placa_destino": "BBB0B00", "descricao": "Transferência normal"}
        ]
    },

    "PF-GAA-T013-DB": {
        "tipo": "tabela_estados",
        "descricao": "Tabela de Estados (UF)",
        "campos": [
            {
                "nome": "uf",
                "label": "Estado",
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
            {"uf": "SP", "descricao": "São Paulo"},
            {"uf": "RJ", "descricao": "Rio de Janeiro"}
        ]
    },

    "PF-GAA-T640-DB": {
        "tipo": "tabela_penalidades",
        "descricao": "Tabela de Penalidades",
        "campos": [
            {
                "nome": "codigo_infracao",
                "label": "Código Infração",
                "tipo": "numero",
                "valor": "0001",
                "maxlength": 4
            },
            {
                "nome": "descricao",
                "label": "Descrição",
                "tipo": "texto",
                "valor": "Estacionamento proibido",
                "maxlength": 100
            }
        ],
        "exemplos": [
            {"codigo_infracao": "0001", "descricao": "Estacionamento proibido", "descricao_ex": "Infração leve"},
            {"codigo_infracao": "0010", "descricao": "Dirigir sem habilitação", "descricao_ex": "Infração grave"}
        ]
    },

    # ==================== GEV - Gestão Empadronização Veicular ====================

    "PF-GEV-L006-DB": {
        "tipo": "empadronizacao",
        "descricao": "Gestão de Empadronização Veicular",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            },
            {
                "nome": "ano_fabricacao",
                "label": "Ano de Fabricação",
                "tipo": "numero",
                "valor": "2020",
                "min": "1980",
                "max": "2026"
            },
            {
                "nome": "marca",
                "label": "Marca",
                "tipo": "texto",
                "valor": "Toyota",
                "maxlength": 50
            },
            {
                "nome": "modelo",
                "label": "Modelo",
                "tipo": "texto",
                "valor": "Corolla",
                "maxlength": 50
            }
        ],
        "exemplos": [
            {
                "placa": "AAA0A00",
                "ano_fabricacao": "2020",
                "marca": "Toyota",
                "modelo": "Corolla",
                "descricao": "Veículo Mercosul recente"
            },
            {
                "placa": "SP1234",
                "ano_fabricacao": "2010",
                "marca": "Volkswagen",
                "modelo": "Gol",
                "descricao": "Veículo antigo"
            }
        ]
    },

    "PF-GEV-T005-DB": {
        "tipo": "tabela_combustivel",
        "descricao": "Tabela de Combustíveis",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código",
                "tipo": "numero",
                "valor": "01",
                "maxlength": 2
            },
            {
                "nome": "tipo",
                "label": "Tipo de Combustível",
                "tipo": "select",
                "valor": "GASOLINA",
                "opcoes": [
                    {"valor": "GASOLINA", "label": "Gasolina"},
                    {"valor": "DIESEL", "label": "Diesel"},
                    {"valor": "ALCOOL", "label": "Álcool"},
                    {"valor": "GNV", "label": "GNV"},
                    {"valor": "ELETRICO", "label": "Elétrico"}
                ]
            }
        ],
        "exemplos": [
            {"codigo": "01", "tipo": "GASOLINA", "descricao": "Veículo à gasolina"},
            {"codigo": "03", "tipo": "GNV", "descricao": "Veículo GNV"}
        ]
    },

    "PF-GEV-T020-DB": {
        "tipo": "tabela_cores",
        "descricao": "Tabela de Cores",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código",
                "tipo": "numero",
                "valor": "01",
                "maxlength": 2
            },
            {
                "nome": "cor",
                "label": "Cor",
                "tipo": "select",
                "valor": "BRANCO",
                "opcoes": [
                    {"valor": "BRANCO", "label": "Branco"},
                    {"valor": "PRETO", "label": "Preto"},
                    {"valor": "PRATA", "label": "Prata"},
                    {"valor": "CINZA", "label": "Cinza"},
                    {"valor": "VERMELHO", "label": "Vermelho"},
                    {"valor": "AZUL", "label": "Azul"}
                ]
            }
        ],
        "exemplos": [
            {"codigo": "01", "cor": "BRANCO", "descricao": "Branco"},
            {"codigo": "10", "cor": "PRETO", "descricao": "Preto"}
        ]
    },

    "PF-GEV-T021-DB": {
        "tipo": "tabela_categorias",
        "descricao": "Tabela de Categorias Veiculares",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código",
                "tipo": "numero",
                "valor": "01",
                "maxlength": 2
            },
            {
                "nome": "categoria",
                "label": "Categoria",
                "tipo": "select",
                "valor": "AUTOMOVEL",
                "opcoes": [
                    {"valor": "AUTOMOVEL", "label": "Automóvel"},
                    {"valor": "CAMIONETA", "label": "Camioneta"},
                    {"valor": "CAMINHAO", "label": "Caminhão"},
                    {"valor": "MOTOCICLETA", "label": "Motocicleta"},
                    {"valor": "ONIBUS", "label": "Ônibus"}
                ]
            }
        ],
        "exemplos": [
            {"codigo": "01", "categoria": "AUTOMOVEL", "descricao": "Automóvel"},
            {"codigo": "09", "categoria": "MOTOCICLETA", "descricao": "Motocicleta"}
        ]
    },

    "PF-GEV-T050-DB": {
        "tipo": "tabela_marcas",
        "descricao": "Tabela de Marcas Veiculares",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código",
                "tipo": "numero",
                "valor": "001",
                "maxlength": 3
            },
            {
                "nome": "marca",
                "label": "Marca",
                "tipo": "texto",
                "valor": "TOYOTA",
                "maxlength": 50
            }
        ],
        "exemplos": [
            {"codigo": "001", "marca": "TOYOTA", "descricao": "Toyota"},
            {"codigo": "002", "marca": "VOLKSWAGEN", "descricao": "Volkswagen"},
            {"codigo": "003", "marca": "FIAT", "descricao": "Fiat"}
        ]
    },

    "PF-GEV-T430-DB": {
        "tipo": "tabela_circunscritos",
        "descricao": "Tabela de Circunscrições",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código",
                "tipo": "numero",
                "valor": "0001",
                "maxlength": 4
            },
            {
                "nome": "descricao",
                "label": "Descrição",
                "tipo": "texto",
                "valor": "Circunscrição Centro",
                "maxlength": 100
            },
            {
                "nome": "uf",
                "label": "UF",
                "tipo": "select",
                "valor": "SP",
                "opcoes": [
                    {"valor": "SP", "label": "São Paulo"},
                    {"valor": "RJ", "label": "Rio de Janeiro"}
                ]
            }
        ],
        "exemplos": [
            {
                "codigo": "0001",
                "descricao": "Circunscrição Centro",
                "uf": "SP",
                "descricao_ex": "Centro de São Paulo"
            }
        ]
    },

    # ==================== GAT - Gestão Autoridades ====================

    "PF-GAT-L006-DB": {
        "tipo": "gestao_autoridades",
        "descricao": "Gestão de Autoridades de Trânsito",
        "campos": [
            {
                "nome": "codigo_autoridade",
                "label": "Código Autoridade",
                "tipo": "numero",
                "valor": "001",
                "min": "001",
                "max": "999"
            },
            {
                "nome": "nome_autoridade",
                "label": "Nome da Autoridade",
                "tipo": "texto",
                "valor": "DETRAN SP",
                "maxlength": 100
            },
            {
                "nome": "uf",
                "label": "Estado",
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
                "codigo_autoridade": "001",
                "nome_autoridade": "DETRAN SP",
                "uf": "SP",
                "descricao": "DETRAN São Paulo"
            },
            {
                "codigo_autoridade": "002",
                "nome_autoridade": "DETRAN RJ",
                "uf": "RJ",
                "descricao": "DETRAN Rio de Janeiro"
            }
        ]
    },

    "PF-GAT-T030-DB": {
        "tipo": "tabela_penalidades_autoridade",
        "descricao": "Tabela de Penalidades por Autoridade",
        "campos": [
            {
                "nome": "codigo_autoridade",
                "label": "Código Autoridade",
                "tipo": "numero",
                "valor": "001",
                "max": "999"
            },
            {
                "nome": "codigo_infracao",
                "label": "Código Infração",
                "tipo": "numero",
                "valor": "0001",
                "maxlength": 4
            },
            {
                "nome": "pontos",
                "label": "Pontos",
                "tipo": "numero",
                "valor": "3",
                "min": "0",
                "max": "20"
            }
        ],
        "exemplos": [
            {
                "codigo_autoridade": "001",
                "codigo_infracao": "0001",
                "pontos": "3",
                "descricao": "Penalidade leve"
            },
            {
                "codigo_autoridade": "001",
                "codigo_infracao": "0002",
                "pontos": "20",
                "descricao": "Penalidade grave"
            }
        ]
    },

    # ==================== Padrão para programas sem dados específicos ====================

    "DEFAULT": {
        "tipo": "generico",
        "descricao": "Programa COBOL Genérico",
        "campos": [
            {
                "nome": "entrada",
                "label": "Dados de Entrada",
                "tipo": "textarea",
                "placeholder": "Digite os dados de entrada",
                "valor": "Insira dados aqui",
                "rows": 5
            }
        ],
        "exemplos": []
    }
}


def get_mock_data(programa_nome):
    """Retorna dados mockados para um programa"""
    # Verificar se programa existe
    if programa_nome in MOCK_DATA_EXPANDED:
        return MOCK_DATA_EXPANDED[programa_nome]

    # Verificar se é um programa GEV/GAT/GAA genérico
    if programa_nome.startswith("PF-GEV-"):
        return _get_gev_generico(programa_nome)
    elif programa_nome.startswith("PF-GAT-"):
        return _get_gat_generico(programa_nome)
    elif programa_nome.startswith("PF-GAA-"):
        return _get_gaa_generico(programa_nome)
    else:
        return MOCK_DATA_EXPANDED["DEFAULT"]


def _get_gaa_generico(programa_nome):
    """Retorna dados genéricos para programas GAA não configurados"""
    return {
        "tipo": "gaa_generico",
        "descricao": f"Programa GAA - {programa_nome}",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            }
        ],
        "campos_valor": {"placa": "AAA0A00"},
        "exemplos": [
            {"placa": "AAA0A00", "descricao": "Exemplo padrão"}
        ]
    }


def _get_gev_generico(programa_nome):
    """Retorna dados genéricos para programas GEV não configurados"""
    return {
        "tipo": "gev_generico",
        "descricao": f"Programa GEV - {programa_nome}",
        "campos": [
            {
                "nome": "placa",
                "label": "Placa",
                "tipo": "texto",
                "valor": "AAA0A00",
                "maxlength": 10
            },
            {
                "nome": "dados",
                "label": "Dados Adicionais",
                "tipo": "textarea",
                "valor": "Informações do veículo",
                "rows": 3
            }
        ],
        "campos_valor": {
            "placa": "AAA0A00",
            "dados": "Informações do veículo"
        },
        "exemplos": [
            {
                "placa": "AAA0A00",
                "dados": "Dados de exemplo",
                "descricao": "Exemplo padrão"
            }
        ]
    }


def _get_gat_generico(programa_nome):
    """Retorna dados genéricos para programas GAT não configurados"""
    return {
        "tipo": "gat_generico",
        "descricao": f"Programa GAT - {programa_nome}",
        "campos": [
            {
                "nome": "codigo",
                "label": "Código",
                "tipo": "numero",
                "valor": "001",
                "maxlength": 3
            },
            {
                "nome": "dados",
                "label": "Dados",
                "tipo": "textarea",
                "valor": "Informações da autoridade",
                "rows": 3
            }
        ],
        "campos_valor": {
            "codigo": "001",
            "dados": "Informações da autoridade"
        },
        "exemplos": [
            {
                "codigo": "001",
                "dados": "Dados de exemplo",
                "descricao": "Exemplo padrão"
            }
        ]
    }


def validar_entrada(programa_nome, dados):
    """Valida dados de entrada para um programa"""
    # Se não há dados, aceitar (permite execução com valores padrão)
    if not dados:
        return {"valido": True, "erros": []}

    mock = get_mock_data(programa_nome)
    erros = []

    for campo in mock.get("campos", []):
        nome_campo = campo["nome"]
        tipo_campo = campo["tipo"]

        # Se o campo não foi enviado, pular (usar valor padrão)
        if nome_campo not in dados:
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


def get_todos_programas_com_dados():
    """Retorna lista de programas que têm dados mockados"""
    return list(MOCK_DATA_EXPANDED.keys())
