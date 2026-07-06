"""
Mapeamento entre programas originais (Micro Focus .C74) e convertidos (GnuCOBOL).

Convenção de nomes convertidos:
- FGAA = PF-GAA-L (Funcao GAA - Leitura/Validacao)
- OGAA = PF-GAA-T (Online GAA - Transacao)
- PGAA = PF-GAA-B (Processador GAA - Batch/DB)
- FGAT = PF-GAT-L (Funcao GAT)
- FGEV = PF-GEV-L (Funcao GEV)
- OGEV = PF-GEV-T (Online GEV)

Programas auxiliares (COPY/MAPA) nao tem equivalente direto nos originais:
- AUML01, CAPA01, CCCC99, COFI02, COFI04, COFI11, EMIS98, EMIS99,
  EMPA01, GERA01, MENS01, MENS03, RENA01, RENA04
"""

# Mapeamento: original -> convertido
PROGRAM_MAP = {
    # GAA - Gestao Arquivo Automotivo (Leitura/Validacao)
    "PF-GAA-L004": "FGAA004",
    "PF-GAA-L005": "FGAA005",
    "PF-GAA-L007": "FGAA007",
    "PF-GAA-L012-DB": "FGAA012D",
    "PF-GAA-L015": "FGAA015",
    "PF-GAA-L032-DB": "FGAA032D",
    "PF-GAA-L050-DB": "FGAA050D",
    "PF-GAA-L115-DB": "FGAA115D",
    # GAA - Gestao Arquivo Automotivo (Transacoes Online)
    "PF-GAA-T013-DB": "OGAA013D",
    "PF-GAA-T018-DB": "OGAA018D",
    "PF-GAA-T255-DB": "OGAA255D",
    "PF-GAA-T615-DB": "OGAA615D",
    "PF-GAA-T640-DB": "OGAA640D",
    "PF-GAA-T792-DB": "OGAA792D",
    "PF-GAA-T920-DB": "OGAA920D",
    # GAA - Batch/DB
    "PF-GAA-B100-DB": "PGAA100D",
    # GAT - Gestao Autoridades Transito
    "PF-GAT-L006-DB": "FGAT006D",
    "PF-GAT-L030-DB": "FGAT030D",
    # GEV - Gestao Empadronizacao Veicular (Leitura)
    "PF-GEV-L006-DB": "FGEV006D",
    # GEV - Gestao Empadronizacao Veicular (Transacoes Online)
    "PF-GEV-T005-DB": "OGEV005D",
    "PF-GEV-T020-DB": "OGEV020D",
    "PF-GEV-T021-DB": "OGEV021D",
    "PF-GEV-T050-DB": "OGEV050D",
    "PF-GEV-T430-DB": "OGEV430D",
    "PF-GEV-T431-DB": "OGEV431D",
    "PF-GEV-T432-DB": "OGEV432D",
    "PF-GEV-T433-DB": "OGEV433D",
    "PF-GEV-T434-DB": "OGEV434D",
    "PF-GEV-T435-DB": "OGEV435D",
    "PF-GEV-T436-DB": "OGEV436D",
    "PF-GEV-T441-DB": "OGEV441D",
    "PF-GEV-T442-DB": "OGEV442D",
    "PF-GEV-T443-DB": "OGEV443D",
    "PF-GEV-T444-DB": "OGEV444D",
    "PF-GEV-T445-DB": "OGEV445D",
    "PF-GEV-T446-DB": "OGEV446D",
    "PF-GEV-T535-DB": "OGEV535D",
    "PF-GEV-T630-DB": "OGEV630D",
    "PF-GEV-T635-DB": "OGEV635D",
    "PF-GEV-T680-DB": "OGEV680D",
    "PF-GEV-T690-DB": "OGEV690D",
    "PF-GEV-T720-DB": "OGEV720D",
}

# Mapeamento reverso: convertido -> original
REVERSE_MAP = {v: k for k, v in PROGRAM_MAP.items()}

# Programas auxiliares (copybooks, mapas, etc.) - apenas no convertido
AUXILIARY_PROGRAMS = [
    "AUML01", "CAPA01", "CCCC99", "COFI02", "COFI04", "COFI11",
    "EMIS98", "EMIS99", "EMPA01", "GERA01", "MENS01", "MENS03",
    "RENA01", "RENA04",
]

# Categorias
CATEGORIES = {
    "GAA - Gestao Arquivo Automotivo": [
        k for k in PROGRAM_MAP if "GAA" in k
    ],
    "GAT - Gestao Autoridades Transito": [
        k for k in PROGRAM_MAP if "GAT" in k
    ],
    "GEV - Gestao Empadronizacao Veicular": [
        k for k in PROGRAM_MAP if "GEV" in k
    ],
}


def get_converted_name(original_name: str) -> str:
    """Retorna o nome convertido a partir do nome original."""
    # Tentar com e sem sufixo -DB
    if original_name in PROGRAM_MAP:
        return PROGRAM_MAP[original_name]
    # Tentar adicionar -DB
    if f"{original_name}-DB" in PROGRAM_MAP:
        return PROGRAM_MAP[f"{original_name}-DB"]
    # Busca parcial
    for k, v in PROGRAM_MAP.items():
        if original_name in k:
            return v
    return None


def get_original_name(converted_name: str) -> str:
    """Retorna o nome original a partir do nome convertido."""
    return REVERSE_MAP.get(converted_name)


def get_all_programs():
    """Retorna lista de todos os programas com mapeamento."""
    programs = []
    for original, converted in PROGRAM_MAP.items():
        programs.append({
            "original": original,
            "converted": converted,
            "original_file": f"{original}.C74",
            "converted_file": converted,
            "category": next(
                (cat for cat, progs in CATEGORIES.items() if original in progs),
                "Outros"
            ),
        })
    return programs


def get_programs_by_category():
    """Retorna programas agrupados por categoria."""
    result = {}
    for category, originals in CATEGORIES.items():
        result[category] = []
        for orig in originals:
            conv = PROGRAM_MAP.get(orig)
            result[category].append({
                "original": orig,
                "converted": conv,
                "original_file": f"{orig}.C74",
                "converted_file": conv,
            })
    return result
