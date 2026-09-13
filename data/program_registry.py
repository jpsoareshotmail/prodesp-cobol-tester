"""
Registro dinamico de programas COBOL (original -> convertido).

Ao contrario do PROGRAM_MAP hardcoded (data/program_mapping.py), este registro
e reconstruido a partir dos arquivos presentes nas pastas de fontes, permitindo
limpar o projeto e importar fontes novos sem editar codigo.

O mapa e persistido em data/program_map.json. Se o arquivo nao existir, cai no
PROGRAM_MAP hardcoded como semente inicial (compatibilidade).

Convencao de pareamento original -> convertido:
  Originais ficam em fontes_convertidos/Originais/*.C74 (nome ex: PF-GAA-L004-DB.C74)
  Convertidos ficam em fontes_convertidos/Convertidos/<nome> (sem extensao, ex: FGAA004)
  O pareamento vem do proprio PROGRAM_MAP (quando conhecido). Para fontes novos
  sem correspondencia conhecida, cada arquivo entra como um programa avulso
  (original OU convertido), aparecendo assim mesmo na lista.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent
_MAP_FILE = _DATA_DIR / 'program_map.json'
_ROOT = _DATA_DIR.parent
_ORIGINAIS = _ROOT / 'fontes_convertidos' / 'Originais'
_CONVERTIDOS = _ROOT / 'fontes_convertidos' / 'Convertidos'


def _semente_hardcoded() -> dict:
    try:
        from data.program_mapping import PROGRAM_MAP
        return dict(PROGRAM_MAP)
    except Exception:
        return {}


def carregar_mapa() -> dict:
    """Retorna o mapa original->convertido (do JSON persistido ou da semente)."""
    if _MAP_FILE.exists():
        try:
            return json.loads(_MAP_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return _semente_hardcoded()


def salvar_mapa(mapa: dict) -> None:
    _MAP_FILE.write_text(json.dumps(mapa, indent=2, ensure_ascii=False), encoding='utf-8')


def _categoria(nome: str) -> str:
    u = (nome or '').upper()
    if 'GAA' in u:
        return 'GAA - Gestao Arquivo Automotivo'
    if 'GAT' in u:
        return 'GAT - Gestao Autoridades Transito'
    if 'GEV' in u:
        return 'GEV - Gestao Empadronizacao Veicular'
    return 'Outros'


def _eh_programa_cobol(path: Path) -> bool:
    """Heuristica: arquivo de fonte COBOL (tem IDENTIFICATION/PROGRAM-ID)."""
    try:
        txt = path.read_text(encoding='latin-1', errors='ignore')[:8000].upper()
        return 'PROGRAM-ID' in txt or 'IDENTIFICATION DIVISION' in txt
    except Exception:
        return False


def reconstruir_mapa_do_disco() -> dict:
    """Reconstroi o mapa a partir dos arquivos presentes nas pastas de fontes.

    O pareamento original<->convertido usa como referencia o mapa atual (JSON)
    combinado com a semente hardcoded, para ser robusto mesmo quando o JSON
    esta vazio (apos um "Limpar projeto"). Fontes sem par conhecido entram
    como avulsos para aparecerem mesmo assim na lista.
    """
    # referencia de pareamento: semente + mapa atual (o atual tem prioridade)
    conhecido = dict(_semente_hardcoded())
    if _MAP_FILE.exists():
        try:
            atual = json.loads(_MAP_FILE.read_text(encoding='utf-8'))
            if isinstance(atual, dict):
                conhecido.update({k: v for k, v in atual.items() if v})
        except Exception:
            pass
    reverso = {v: k for k, v in conhecido.items() if v}

    # arquivos presentes em disco
    originais = set()
    if _ORIGINAIS.exists():
        for f in _ORIGINAIS.iterdir():
            if f.is_file() and f.suffix.lower() in ('.c74', '.cob') and not f.name.upper().startswith('MAPA_'):
                originais.add(f.stem.upper())

    convertidos = set()
    if _CONVERTIDOS.exists():
        for f in _CONVERTIDOS.iterdir():
            if f.is_file() and _eh_programa_cobol(f):
                convertidos.add(f.name)

    novo = {}
    usados_conv = set()

    # 1. para cada original em disco, tenta achar o convertido correspondente
    for orig_upper in originais:
        # recupera a grafia original conhecida (preserva case/hifens)
        orig = next((k for k in conhecido if k.upper() == orig_upper), orig_upper)
        conv = conhecido.get(orig) or conhecido.get(f'{orig}-DB') or ''
        if conv and conv in convertidos:
            novo[orig] = conv
            usados_conv.add(conv)
        elif conv:
            # convertido conhecido mas ausente em disco: registra so o original
            novo[orig] = conv if conv in convertidos else ''
            if conv in convertidos:
                usados_conv.add(conv)
        else:
            novo[orig] = ''

    # 2. convertidos em disco ainda nao pareados
    for conv in convertidos:
        if conv in usados_conv:
            continue
        orig = reverso.get(conv)
        if orig and orig not in novo:
            novo[orig] = conv
            usados_conv.add(conv)
        elif not orig:
            # convertido novo sem original conhecido: entra com chave propria
            chave = f'(novo) {conv}'
            novo.setdefault(chave, conv)
            usados_conv.add(conv)

    salvar_mapa(novo)
    return novo


def programas_por_categoria() -> dict:
    """Agrupa os programas do mapa por categoria (para a sidebar)."""
    mapa = carregar_mapa()
    result = {}
    for original, convertido in sorted(mapa.items()):
        cat = _categoria(original + ' ' + (convertido or ''))
        result.setdefault(cat, []).append({
            'original': original,
            'converted': convertido,
            'original_file': f'{original}.C74',
            'converted_file': convertido,
        })
    return result


def total_programas() -> int:
    return len(carregar_mapa())
