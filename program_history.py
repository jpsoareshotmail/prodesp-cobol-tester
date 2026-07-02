#!/usr/bin/env python3
"""
Histórico de Versões e Alterações dos Programas COBOL
Rastreia autor, data e alterações efetuadas em cada programa
"""

PROGRAM_HISTORY = {
    "PF-GAA-L004": {
        "autor": "Carlos Silva",
        "criacao": "2023-01-10",
        "versao_atual": "3.2",
        "alteracoes": [
            {"data": "2026-07-02", "pessoa": "Ana Costa", "tipo": "Manutenção", "descricao": "Adicionado suporte a placas Mercosul"},
            {"data": "2026-06-15", "pessoa": "Bruno Santos", "tipo": "Bug Fix", "descricao": "Corrigido bug na validação de placas antigas"},
            {"data": "2026-05-20", "pessoa": "Carlos Silva", "tipo": "Feature", "descricao": "Implementado validador de placas de 2 letras"},
            {"data": "2023-01-10", "pessoa": "Carlos Silva", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L005": {
        "autor": "Mariana Lima",
        "criacao": "2023-02-05",
        "versao_atual": "2.1",
        "alteracoes": [
            {"data": "2026-06-30", "pessoa": "Mariana Lima", "tipo": "Manutenção", "descricao": "Otimização de consultas ao banco"},
            {"data": "2026-04-10", "pessoa": "João Pedro", "tipo": "Feature", "descricao": "Adicionado filtro por marca e modelo"},
            {"data": "2023-02-05", "pessoa": "Mariana Lima", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L007": {
        "autor": "Roberto Alves",
        "criacao": "2023-03-12",
        "versao_atual": "1.8",
        "alteracoes": [
            {"data": "2026-07-01", "pessoa": "Roberto Alves", "tipo": "Bug Fix", "descricao": "Validação de CRVA mais rigorosa"},
            {"data": "2026-03-05", "pessoa": "Fernanda Costa", "tipo": "Feature", "descricao": "Adicionado suporte a novos tipos de documentos"},
            {"data": "2023-03-12", "pessoa": "Roberto Alves", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-B100-DB": {
        "autor": "Patricia Gomes",
        "criacao": "2023-01-20",
        "versao_atual": "2.5",
        "alteracoes": [
            {"data": "2026-06-25", "pessoa": "Patricia Gomes", "tipo": "Performance", "descricao": "Implementado índices para melhorar busca"},
            {"data": "2026-04-15", "pessoa": "Marcos Silva", "tipo": "Feature", "descricao": "Adicionado filtro por estado"},
            {"data": "2023-01-20", "pessoa": "Patricia Gomes", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L012-DB": {
        "autor": "Lucia Ferreira",
        "criacao": "2023-04-08",
        "versao_atual": "1.9",
        "alteracoes": [
            {"data": "2026-06-20", "pessoa": "Lucia Ferreira", "tipo": "Manutenção", "descricao": "Correção na numeração de documentos"},
            {"data": "2026-02-14", "pessoa": "Thiago Oliveira", "tipo": "Feature", "descricao": "Suporte a emissão de CRV digital"},
            {"data": "2023-04-08", "pessoa": "Lucia Ferreira", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L015": {
        "autor": "Felipe Mendes",
        "criacao": "2023-05-15",
        "versao_atual": "1.6",
        "alteracoes": [
            {"data": "2026-07-02", "pessoa": "Felipe Mendes", "tipo": "Feature", "descricao": "Adicionado rastreamento de transferência"},
            {"data": "2026-05-10", "pessoa": "Sandra Rocha", "tipo": "Bug Fix", "descricao": "Corrigido erro na transferência entre estados"},
            {"data": "2023-05-15", "pessoa": "Felipe Mendes", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L032-DB": {
        "autor": "Rafael Costa",
        "criacao": "2023-06-01",
        "versao_atual": "1.4",
        "alteracoes": [
            {"data": "2026-06-15", "pessoa": "Rafael Costa", "tipo": "Manutenção", "descricao": "Atualização de status de registros"},
            {"data": "2023-06-01", "pessoa": "Rafael Costa", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L050-DB": {
        "autor": "Cristina Silva",
        "criacao": "2023-07-10",
        "versao_atual": "1.3",
        "alteracoes": [
            {"data": "2026-06-28", "pessoa": "Cristina Silva", "tipo": "Feature", "descricao": "Integração com POUPA-TEMPO"},
            {"data": "2023-07-10", "pessoa": "Cristina Silva", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-L115-DB": {
        "autor": "Wagner Lima",
        "criacao": "2023-08-05",
        "versao_atual": "1.2",
        "alteracoes": [
            {"data": "2026-06-10", "pessoa": "Wagner Lima", "tipo": "Manutenção", "descricao": "Melhorias na consulta de dados"},
            {"data": "2023-08-05", "pessoa": "Wagner Lima", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T013-DB": {
        "autor": "Beatriz Oliveira",
        "criacao": "2023-09-12",
        "versao_atual": "1.5",
        "alteracoes": [
            {"data": "2026-07-01", "pessoa": "Beatriz Oliveira", "tipo": "Feature", "descricao": "Adicionado validação de multas"},
            {"data": "2023-09-12", "pessoa": "Beatriz Oliveira", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T018-DB": {
        "autor": "Henrique Rocha",
        "criacao": "2023-10-20",
        "versao_atual": "1.1",
        "alteracoes": [
            {"data": "2026-05-15", "pessoa": "Henrique Rocha", "tipo": "Bug Fix", "descricao": "Corrigido campo de endereço"},
            {"data": "2023-10-20", "pessoa": "Henrique Rocha", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T255-DB": {
        "autor": "Juliana Martins",
        "criacao": "2024-01-08",
        "versao_atual": "1.0",
        "alteracoes": [
            {"data": "2024-01-08", "pessoa": "Juliana Martins", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T615-DB": {
        "autor": "Gustavo Pereira",
        "criacao": "2024-02-14",
        "versao_atual": "1.0",
        "alteracoes": [
            {"data": "2024-02-14", "pessoa": "Gustavo Pereira", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T640-DB": {
        "autor": "Camila Santos",
        "criacao": "2024-03-01",
        "versao_atual": "1.2",
        "alteracoes": [
            {"data": "2026-06-05", "pessoa": "Camila Santos", "tipo": "Manutenção", "descricao": "Otimização de emissão de CRV"},
            {"data": "2024-03-01", "pessoa": "Camila Santos", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T792-DB": {
        "autor": "Leonardo Teixeira",
        "criacao": "2024-04-10",
        "versao_atual": "1.0",
        "alteracoes": [
            {"data": "2024-04-10", "pessoa": "Leonardo Teixeira", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAA-T920-DB": {
        "autor": "Vanessa Gomes",
        "criacao": "2024-05-20",
        "versao_atual": "1.1",
        "alteracoes": [
            {"data": "2026-06-01", "pessoa": "Vanessa Gomes", "tipo": "Feature", "descricao": "Implementado certificado digital"},
            {"data": "2024-05-20", "pessoa": "Vanessa Gomes", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-L006-DB": {
        "autor": "Adriano Costa",
        "criacao": "2023-02-01",
        "versao_atual": "3.0",
        "alteracoes": [
            {"data": "2026-07-02", "pessoa": "Adriano Costa", "tipo": "Feature", "descricao": "Adicionado suporte a empadronização online"},
            {"data": "2026-05-01", "pessoa": "Isabela Martins", "tipo": "Bug Fix", "descricao": "Corrigido sincronização de dados"},
            {"data": "2023-02-01", "pessoa": "Adriano Costa", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-T005-DB": {
        "autor": "Fabio Almeida",
        "criacao": "2023-03-10",
        "versao_atual": "2.0",
        "alteracoes": [
            {"data": "2026-06-20", "pessoa": "Fabio Almeida", "tipo": "Feature", "descricao": "Adicionado novos tipos de combustível"},
            {"data": "2023-03-10", "pessoa": "Fabio Almeida", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-T020-DB": {
        "autor": "Simone Barbosa",
        "criacao": "2023-04-05",
        "versao_atual": "1.8",
        "alteracoes": [
            {"data": "2026-06-10", "pessoa": "Simone Barbosa", "tipo": "Manutenção", "descricao": "Atualização de paleta de cores"},
            {"data": "2023-04-05", "pessoa": "Simone Barbosa", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-T021-DB": {
        "autor": "Ricardo Dias",
        "criacao": "2023-05-15",
        "versao_atual": "1.5",
        "alteracoes": [
            {"data": "2026-05-20", "pessoa": "Ricardo Dias", "tipo": "Feature", "descricao": "Adicionado categoria de eletromóveis"},
            {"data": "2023-05-15", "pessoa": "Ricardo Dias", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-T050-DB": {
        "autor": "Monica Torres",
        "criacao": "2023-06-01",
        "versao_atual": "2.2",
        "alteracoes": [
            {"data": "2026-06-15", "pessoa": "Monica Torres", "tipo": "Feature", "descricao": "Adicionado marcas chinesas"},
            {"data": "2023-06-01", "pessoa": "Monica Torres", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-T430-DB": {
        "autor": "Sergio Barbosa",
        "criacao": "2023-07-10",
        "versao_atual": "1.3",
        "alteracoes": [
            {"data": "2026-04-05", "pessoa": "Sergio Barbosa", "tipo": "Manutenção", "descricao": "Atualização de circunscrições"},
            {"data": "2023-07-10", "pessoa": "Sergio Barbosa", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GEV-T431-DB": {"autor": "Paula Souza", "criacao": "2024-01-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-01-15", "pessoa": "Paula Souza", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T432-DB": {"autor": "Oliver Schmidt", "criacao": "2024-02-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-02-01", "pessoa": "Oliver Schmidt", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T433-DB": {"autor": "Quentin Brown", "criacao": "2024-02-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-02-15", "pessoa": "Quentin Brown", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T434-DB": {"autor": "Rosana Silva", "criacao": "2024-03-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-03-01", "pessoa": "Rosana Silva", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T435-DB": {"autor": "Samuel Costa", "criacao": "2024-03-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-03-15", "pessoa": "Samuel Costa", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T436-DB": {"autor": "Tatiana Gomes", "criacao": "2024-04-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-04-01", "pessoa": "Tatiana Gomes", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T441-DB": {"autor": "Ulisses Pereira", "criacao": "2024-04-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-04-15", "pessoa": "Ulisses Pereira", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T442-DB": {"autor": "Vanessa Lima", "criacao": "2024-05-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-05-01", "pessoa": "Vanessa Lima", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T443-DB": {"autor": "Wagner Silva", "criacao": "2024-05-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-05-15", "pessoa": "Wagner Silva", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T444-DB": {"autor": "Xavier Costa", "criacao": "2024-06-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-06-01", "pessoa": "Xavier Costa", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T445-DB": {"autor": "Yara Martins", "criacao": "2024-06-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-06-15", "pessoa": "Yara Martins", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T446-DB": {"autor": "Zelia Ferreira", "criacao": "2024-07-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-07-01", "pessoa": "Zelia Ferreira", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T535-DB": {"autor": "Alice Santos", "criacao": "2024-07-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-07-15", "pessoa": "Alice Santos", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T630-DB": {"autor": "Bruno Oliveira", "criacao": "2024-08-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-08-01", "pessoa": "Bruno Oliveira", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T635-DB": {"autor": "Carla Costa", "criacao": "2024-08-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-08-15", "pessoa": "Carla Costa", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T680-DB": {"autor": "Denise Silva", "criacao": "2024-09-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-09-01", "pessoa": "Denise Silva", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T690-DB": {"autor": "Edmundo Pereira", "criacao": "2024-09-15", "versao_atual": "1.0", "alteracoes": [{"data": "2024-09-15", "pessoa": "Edmundo Pereira", "tipo": "Criação", "descricao": "Programa criado"}]},
    "PF-GEV-T720-DB": {"autor": "Fernanda Gomes", "criacao": "2024-10-01", "versao_atual": "1.0", "alteracoes": [{"data": "2024-10-01", "pessoa": "Fernanda Gomes", "tipo": "Criação", "descricao": "Programa criado"}]},

    "PF-GAT-L006-DB": {
        "autor": "Gisele Rocha",
        "criacao": "2023-08-20",
        "versao_atual": "1.5",
        "alteracoes": [
            {"data": "2026-06-20", "pessoa": "Gisele Rocha", "tipo": "Feature", "descricao": "Adicionado suporte a novas autoridades"},
            {"data": "2023-08-20", "pessoa": "Gisele Rocha", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    },

    "PF-GAT-T030-DB": {
        "autor": "Higor Silva",
        "criacao": "2023-09-25",
        "versao_atual": "2.0",
        "alteracoes": [
            {"data": "2026-07-02", "pessoa": "Higor Silva", "tipo": "Feature", "descricao": "Atualizado valores de multas 2026"},
            {"data": "2026-01-01", "pessoa": "Higor Silva", "tipo": "Manutenção", "descricao": "Ajuste de penalidades"},
            {"data": "2023-09-25", "pessoa": "Higor Silva", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    }
}


def get_program_history(programa_nome):
    """Retorna histórico de um programa específico"""
    if programa_nome in PROGRAM_HISTORY:
        return PROGRAM_HISTORY[programa_nome]
    return {
        "autor": "Desconhecido",
        "criacao": "2024-01-01",
        "versao_atual": "1.0",
        "alteracoes": [
            {"data": "2024-01-01", "pessoa": "Sistema", "tipo": "Criação", "descricao": "Programa criado"}
        ]
    }


def get_all_histories():
    """Retorna histórico de todos os programas"""
    return PROGRAM_HISTORY
