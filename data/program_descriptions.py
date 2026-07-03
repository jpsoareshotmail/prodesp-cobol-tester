#!/usr/bin/env python3
"""
Descrições Detalhadas de Todos os 42 Programas COBOL
Usado para exibir informações na interface de seleção
"""

PROGRAM_DESCRIPTIONS = {
    # ==================== GAA - Gestão Arquivo Automotivo ====================

    "PF-GAA-L004": {
        "nome": "Validador de Placas",
        "categoria": "GAA",
        "descricao": "Verifica se a placa está no formato permitido para São Paulo (Mercosul, Antiga, 2 letras). Retorna código indicando o tipo de placa identificado.",
        "objetivo": "Validação de formato de placa veicular",
        "entrada": "Placa (texto até 10 caracteres)",
        "saida": "Código (00-34) e descrição do tipo"
    },

    "PF-GAA-L005": {
        "nome": "Consulta Dados de Veículo",
        "categoria": "GAA",
        "descricao": "Devolve ao chamador a placa formatada com 7 posições no padrão LLLNNNN. Consulta dados básicos do veículo.",
        "objetivo": "Consultar e formatar dados de veículo",
        "entrada": "Placa e documento RENAVAM",
        "saida": "Placa formatada e dados do veículo"
    },

    "PF-GAA-L007": {
        "nome": "Validação de Documentação",
        "categoria": "GAA",
        "descricao": "Substitui L006. Valida placa Mercosul e formatos antigos (2 e 3 letras). Verifica se documentação é válida.",
        "objetivo": "Validar documentação e formato de placa",
        "entrada": "Placa e tipo de documento",
        "saida": "Status de validação e código de retorno"
    },

    "PF-GAA-B100-DB": {
        "nome": "Banco de Dados - Veículos",
        "categoria": "GAA",
        "descricao": "Carrega registros de assinatura digital do banco de dados de veículos. Mantém segurança de documentos.",
        "objetivo": "Carregar registros com autenticação digital",
        "entrada": "Placa ou código de identificação",
        "saida": "Registro com assinatura digital validada"
    },

    "PF-GAA-L012-DB": {
        "nome": "Emissão de Documentos",
        "categoria": "GAA",
        "descricao": "Emite documentos de veículo (CRLV, CRV, DUT). Gera certificados de registro e licenciamento.",
        "objetivo": "Gerar documentos oficiais de registro",
        "entrada": "Placa e tipo de documento",
        "saida": "Documento gerado ou número de emissão"
    },

    "PF-GAA-L015": {
        "nome": "Processamento de Transferência",
        "categoria": "GAA",
        "descricao": "Processa transferência de veículo entre proprietários. Valida dados de chassis e emite novos documentos.",
        "objetivo": "Registrar transferência de propriedade",
        "entrada": "Placa origem e destino, dados novo proprietário",
        "saida": "Confirmação de transferência"
    },

    "PF-GAA-L032-DB": {
        "nome": "Verificação de Registro",
        "categoria": "GAA",
        "descricao": "Verifica se o veículo está registrado no banco de dados. Valida histórico de registros.",
        "objetivo": "Confirmar existência de registro",
        "entrada": "Placa ou RENAVAM",
        "saida": "Status do registro (ativo/inativo)"
    },

    "PF-GAA-L050-DB": {
        "nome": "Verificar CIRETRAN e POUPA-TEMPO",
        "categoria": "GAA",
        "descricao": "Verifica se CIRETRAN é polo e se município pertence aos POUPA-TEMPO. Valida jurisdição.",
        "objetivo": "Validar localização de atendimento",
        "entrada": "CIRETRAN e código de município",
        "saida": "Status de polo e POUPA-TEMPO"
    },

    "PF-GAA-L115-DB": {
        "nome": "Consulta de Dados",
        "categoria": "GAA",
        "descricao": "Consulta dados diversos do veículo no banco de dados. Busca informações completas de registro.",
        "objetivo": "Recuperar informações do banco",
        "entrada": "Identificador de veículo",
        "saida": "Dados completos de registro"
    },

    "PF-GAA-T013-DB": {
        "nome": "Verificação de Bloqueios e Débitos",
        "categoria": "GAA",
        "descricao": "Verifica bloqueios, débitos e incompatibilidades no cadastro. Impede operações com pendências.",
        "objetivo": "Validar situação financeira",
        "entrada": "Placa ou RENAVAM",
        "saida": "Lista de débitos e bloqueios"
    },

    "PF-GAA-T018-DB": {
        "nome": "Cadastrar Dados de Veículo",
        "categoria": "GAA",
        "descricao": "Cadastra dados do veículo zero KM. Consolida informações de GAAT015 e GAAT020.",
        "objetivo": "Registrar novo veículo",
        "entrada": "Dados completos do veículo zero KM",
        "saida": "Confirmação de cadastro"
    },

    "PF-GAA-T255-DB": {
        "nome": "Solicitar Autorização de CRV",
        "categoria": "GAA",
        "descricao": "Solicita autorização para emissão de CRV (Certificado de Registro Veicular). Integra com sistema 227.",
        "objetivo": "Autorizar emissão de certificado",
        "entrada": "Dados de veículo e proprietário",
        "saida": "Autorização de emissão"
    },

    "PF-GAA-T640-DB": {
        "nome": "Emissão de CRV - Interior",
        "categoria": "GAA",
        "descricao": "Emite CRV para veículos do interior. Processa documentação regionalizada.",
        "objetivo": "Gerar CRV para interior de SP",
        "entrada": "Dados de veículo e município",
        "saida": "CRV emitido"
    },

    "PF-GAA-T792-DB": {
        "nome": "Registro Especial",
        "categoria": "GAA",
        "descricao": "Processa registros especiais e casos específicos de veículos. Tratamento de exceções.",
        "objetivo": "Registrar casos especiais",
        "entrada": "Dados especiais de veículo",
        "saida": "Confirmação de registro especial"
    },

    "PF-GAA-T920-DB": {
        "nome": "Assinatura Digital",
        "categoria": "GAA",
        "descricao": "Carrega e valida assinatura digital de registros. Garante autenticidade de documentos.",
        "objetivo": "Autenticar documentos com assinatura digital",
        "entrada": "Registro e certificado digital",
        "saida": "Validação de assinatura"
    },

    # ==================== GEV - Gestão Empadronização Veicular ====================

    "PF-GEV-L006-DB": {
        "nome": "Gestão de Empadronização Veicular",
        "categoria": "GEV",
        "descricao": "Gerencia todo o processo de empadronização de veículos. Coordena licenciamento, placas e documentos.",
        "objetivo": "Processar empadronização completa",
        "entrada": "Placa, ano, marca, modelo",
        "saida": "Documentação de empadronização"
    },

    "PF-GEV-T005-DB": {
        "nome": "Tabela de Combustíveis",
        "categoria": "GEV",
        "descricao": "Pesquisa no banco de dados para retornar mapas de combustíveis disponíveis. Suporta múltiplos tipos.",
        "objetivo": "Consultar tipos de combustível",
        "entrada": "Código de combustível",
        "saida": "Descrição e características do combustível"
    },

    "PF-GEV-T020-DB": {
        "nome": "Tabela de Cores",
        "categoria": "GEV",
        "descricao": "Consulta tabela de cores válidas para veículos. Mantém lista padronizada de cores.",
        "objetivo": "Recuperar cores disponíveis",
        "entrada": "Código de cor",
        "saida": "Descrição da cor"
    },

    "PF-GEV-T021-DB": {
        "nome": "Tabela de Categorias Veiculares",
        "categoria": "GEV",
        "descricao": "Consulta categorias de veículos (automóvel, caminhão, moto, ônibus). Define tipo de veículo.",
        "objetivo": "Classificar tipo de veículo",
        "entrada": "Código de categoria",
        "saida": "Descrição e características da categoria"
    },

    "PF-GEV-T050-DB": {
        "nome": "Tabela de Marcas Veiculares",
        "categoria": "GEV",
        "descricao": "Consulta marcas de veículos registradas. Mantém cadastro padronizado de fabricantes.",
        "objetivo": "Recuperar marcas cadastradas",
        "entrada": "Código de marca",
        "saida": "Descrição da marca"
    },

    "PF-GEV-T430-DB": {
        "nome": "Tabela de Circunscrições",
        "categoria": "GEV",
        "descricao": "Retorna lista de placas sorteadas para veículo novo. Integra sorteio com empadronização.",
        "objetivo": "Consultar circunscrições por região",
        "entrada": "Código de circunscrição",
        "saida": "Dados da circunscrição e placas disponíveis"
    },

    "PF-GEV-T431-DB": {
        "nome": "Processar Seleção de Placa",
        "categoria": "GEV",
        "descricao": "Processa a seleção de placa pelo proprietário. Registra escolha no sistema.",
        "objetivo": "Registrar escolha de placa",
        "entrada": "Placa selecionada e dados do veículo",
        "saida": "Confirmação de seleção"
    },

    "PF-GEV-T432-DB": {
        "nome": "Validar Placa Selecionada",
        "categoria": "GEV",
        "descricao": "Valida se a placa selecionada está disponível e em conformidade. Verifica duplicação.",
        "objetivo": "Confirmar disponibilidade de placa",
        "entrada": "Placa para validação",
        "saida": "Status de disponibilidade"
    },

    "PF-GEV-T433-DB": {
        "nome": "Confirmar Seleção",
        "categoria": "GEV",
        "descricao": "Confirma a seleção de placa de forma definitiva. Bloqueia placa para o proprietário.",
        "objetivo": "Finalizar seleção de placa",
        "entrada": "Dados de confirmação",
        "saida": "Placa confirmada e empadronização iniciada"
    },

    "PF-GEV-T434-DB": {
        "nome": "Cancelar Seleção de Placa",
        "categoria": "GEV",
        "descricao": "Cancela seleção anterior de placa personalizada. Libera placa para nova seleção.",
        "objetivo": "Reverter seleção de placa",
        "entrada": "Placa a ser cancelada",
        "saida": "Confirmação de cancelamento"
    },

    "PF-GEV-T435-DB": {
        "nome": "Alterar Seleção de Placa",
        "categoria": "GEV",
        "descricao": "Permite alterar placa selecionada dentro do período permitido.",
        "objetivo": "Modificar escolha de placa",
        "entrada": "Placa anterior e nova placa",
        "saida": "Confirmação de alteração"
    },

    "PF-GEV-T436-DB": {
        "nome": "Histórico de Seleções",
        "categoria": "GEV",
        "descricao": "Consulta histórico de seleções de placa do proprietário. Rastreia todas as tentativas.",
        "objetivo": "Recuperar histórico de placas",
        "entrada": "Identificador do proprietário",
        "saida": "Lista de seleções anteriores"
    },

    "PF-GEV-T441-DB": {
        "nome": "Licenciamento Zero KM - Fase 1",
        "categoria": "GEV",
        "descricao": "Fase 1 do licenciamento de veículo zero KM. Executar com opção de escolha de placa para portal.",
        "objetivo": "Iniciar licenciamento de novo veículo",
        "entrada": "Dados de veículo zero KM",
        "saida": "Fase 1 concluída, placa selecionada"
    },

    "PF-GEV-T442-DB": {
        "nome": "Licenciamento - Fase 2",
        "categoria": "GEV",
        "descricao": "Fase 2 do licenciamento. Validação de documentação completa.",
        "objetivo": "Validar documentação",
        "entrada": "Documentos de veículo",
        "saida": "Fase 2 concluída"
    },

    "PF-GEV-T443-DB": {
        "nome": "Licenciamento - Fase 3",
        "categoria": "GEV",
        "descricao": "Fase 3 do licenciamento. Emissão final de CRLV.",
        "objetivo": "Gerar CRLV final",
        "entrada": "Dados validados",
        "saida": "CRLV emitido"
    },

    "PF-GEV-T444-DB": {
        "nome": "Cancelamento de Licenciamento",
        "categoria": "GEV",
        "descricao": "Cancela licenciamento de veículo. Remove de circulação ou revert processo.",
        "objetivo": "Cancelar licenciamento",
        "entrada": "Placa a ser cancelada",
        "saida": "Confirmação de cancelamento"
    },

    "PF-GEV-T445-DB": {
        "nome": "Renovação de Licenciamento",
        "categoria": "GEV",
        "descricao": "Renova licenciamento anual de veículo. Gera novo CRLV.",
        "objetivo": "Renovar licenciamento anual",
        "entrada": "Placa e dados atualizados",
        "saida": "Nova CRLV emitida"
    },

    "PF-GEV-T446-DB": {
        "nome": "Análise de Licenciamento",
        "categoria": "GEV",
        "descricao": "Analisa status de licenciamento de veículo. Identifica pendências.",
        "objetivo": "Consultar status de licenciamento",
        "entrada": "Placa",
        "saida": "Status detalhado de licenciamento"
    },

    "PF-GEV-T535-DB": {
        "nome": "Integração com Portal",
        "categoria": "GEV",
        "descricao": "Integra sistema com portal DETRAN. Sincroniza dados em tempo real.",
        "objetivo": "Integrar com portal oficial",
        "entrada": "Dados de sincronização",
        "saida": "Status de integração"
    },

    "PF-GEV-T630-DB": {
        "nome": "Sincronização de Dados",
        "categoria": "GEV",
        "descricao": "Sincroniza dados entre sistemas. Garante consistência de informações.",
        "objetivo": "Manter dados sincronizados",
        "entrada": "Dados a sincronizar",
        "saida": "Status de sincronização"
    },

    "PF-GEV-T635-DB": {
        "nome": "Validação de Portal",
        "categoria": "GEV",
        "descricao": "Valida dados no portal DETRAN. Garante conformidade com sistema oficial.",
        "objetivo": "Validar dados do portal",
        "entrada": "Dados do portal",
        "saida": "Status de validação"
    },

    "PF-GEV-T680-DB": {
        "nome": "Licenciamento Zero KM - Portal",
        "categoria": "GEV",
        "descricao": "Executa fase 1 do licenciamento de veículo zero KM com opção de escolha de placa via portal.",
        "objetivo": "Licenciar zero KM via portal",
        "entrada": "Dados de veículo e acesso portal",
        "saida": "Acesso ao portal de seleção de placa"
    },

    "PF-GEV-T690-DB": {
        "nome": "Processamento Portal",
        "categoria": "GEV",
        "descricao": "Processa requisições do portal DETRAN. Interface entre web e sistema legado.",
        "objetivo": "Processar requisições web",
        "entrada": "Requisição do portal",
        "saida": "Resposta formatada para portal"
    },

    "PF-GEV-T720-DB": {
        "nome": "Consultas Portal",
        "categoria": "GEV",
        "descricao": "Executa consultas do portal DETRAN. Retorna informações formatadas.",
        "objetivo": "Responder consultas web",
        "entrada": "Query de consulta",
        "saida": "Dados formatados para portal"
    },

    # ==================== GAT - Gestão Autoridades de Trânsito ====================

    "PF-GAT-L006-DB": {
        "nome": "Gestão de Autoridades de Trânsito",
        "categoria": "GAT",
        "descricao": "Gerencia autoridades de trânsito (DETRAN, polícia militar). Registra jurisdições e competências.",
        "objetivo": "Consultar e gerenciar autoridades",
        "entrada": "Código de autoridade e dados",
        "saida": "Informações da autoridade"
    },

    "PF-GAT-T030-DB": {
        "nome": "Tabela de Penalidades",
        "categoria": "GAT",
        "descricao": "Tabela de infrações e penalidades de trânsito. Define pontos, multas e restrições.",
        "objetivo": "Consultar penalidades",
        "entrada": "Código de infração",
        "saida": "Descrição, pontos e valor de multa"
    },
}


def get_program_description(programa_nome):
    """Retorna descrição detalhada de um programa"""
    return PROGRAM_DESCRIPTIONS.get(programa_nome, {
        "nome": programa_nome,
        "categoria": "Desconhecida",
        "descricao": "Programa COBOL do sistema DETRAN/PRODESP",
        "objetivo": "Processar dados veiculares",
        "entrada": "Dados estruturados",
        "saida": "Resultado do processamento"
    })


def get_all_programs_with_descriptions():
    """Retorna lista de todos os programas com descrições"""
    return PROGRAM_DESCRIPTIONS
