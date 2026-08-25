"""
Parser de copybook COBOL.

Le um arquivo .cpy (ou trecho de codigo) e devolve uma arvore de campos com
todos os atributos necessarios para gerar DDL e massa de dados:

  - nivel (01, 05, 07, ...)
  - nome do campo (ou FILLER)
  - PICTURE / PIC decodificado: tipo, tamanho, casas decimais, sinal
  - USAGE (DISPLAY, COMP, COMP-3, COMP-4/BINARY, COMP-1/2)
  - OCCURS (n) para arrays
  - REDEFINES (nome do campo redefinido)
  - nullable (heuristica: grupo/campo terminado em -NUL, comum na conversao DMS->DB2)
  - VALUE (clausula de valor inicial, se houver)

Suporta os formatos vistos no projeto:
  05  CAMPO           PICTURE X(010).
  09  CAMPO           PIC  9(011).
  07  GRUPO-NUL.
  01  REG REDEFINES C-MAPA.
  10  TAB OCCURS 12 TIMES.
  05  VALOR           PIC S9(7)V99 COMP-3.

O parser ignora linhas de comentario (col 7 = '*' ou linha iniciada por '*').
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Modelo de dados
# ---------------------------------------------------------------------------
@dataclass
class PicInfo:
    """Resultado da decodificacao de uma clausula PICTURE."""
    raw: str                     # texto original do PIC
    category: str                # 'alfanumerico' | 'numerico' | 'numerico-editado' | 'desconhecido'
    length: int                  # total de digitos/caracteres (parte inteira + decimal p/ numerico)
    integer_digits: int = 0      # digitos antes do V
    decimal_digits: int = 0      # digitos depois do V
    signed: bool = False         # tem S
    usage: str = 'DISPLAY'       # DISPLAY | COMP | COMP-3 | COMP-4 | COMP-1 | COMP-2

    @property
    def storage_length(self) -> int:
        """Bytes ocupados (aproximado) conforme usage."""
        if self.usage == 'COMP-3':
            return (self.integer_digits + self.decimal_digits) // 2 + 1
        if self.usage in ('COMP', 'COMP-4', 'BINARY'):
            d = self.integer_digits + self.decimal_digits
            if d <= 4:
                return 2
            if d <= 9:
                return 4
            return 8
        return self.length


@dataclass
class Field:
    level: int
    name: str
    pic: Optional[PicInfo] = None
    occurs: int = 0
    redefines: Optional[str] = None
    value: Optional[str] = None
    nullable: bool = False
    is_filler: bool = False
    children: list = field(default_factory=list)

    @property
    def is_group(self) -> bool:
        return self.pic is None and not self.is_filler or bool(self.children)

    @property
    def is_elementary(self) -> bool:
        return self.pic is not None


# ---------------------------------------------------------------------------
# Decodificacao de PICTURE
# ---------------------------------------------------------------------------
_PIC_TOKEN = re.compile(r'([9XASVP9])(?:\((\d+)\))?', re.IGNORECASE)


def parse_pic(pic_text: str, usage: str = 'DISPLAY') -> PicInfo:
    """Decodifica uma string PICTURE em PicInfo.

    Exemplos aceitos:
      X(010)          -> alfanumerico, len 10
      9(011)          -> numerico, 11 digitos
      S9(7)V99        -> numerico com sinal, 7 int + 2 dec
      9(5)V9(3)       -> 5 int + 3 dec
      XXX             -> alfanumerico len 3
      9(4) COMP-3     -> packed
    """
    raw = pic_text.strip().rstrip('.')
    text = raw.upper()

    signed = 'S' in text
    # separa parte inteira x decimal pelo 'V' (ponto decimal implicito)
    if 'V' in text:
        int_part, dec_part = text.split('V', 1)
    else:
        int_part, dec_part = text, ''

    def count_digits(part: str, symbol_set: str) -> int:
        total = 0
        for m in re.finditer(r'([9XASP])(?:\((\d+)\))?', part):
            sym, rep = m.group(1), m.group(2)
            if sym in symbol_set:
                total += int(rep) if rep else 1
        return total

    is_alpha = 'X' in text or 'A' in text
    if is_alpha:
        length = count_digits(text, 'XA9')
        return PicInfo(raw=raw, category='alfanumerico', length=length, usage=usage)

    int_digits = count_digits(int_part, '9P')
    dec_digits = count_digits(dec_part, '9P')
    total = int_digits + dec_digits
    if total == 0:
        return PicInfo(raw=raw, category='desconhecido', length=0, usage=usage)
    return PicInfo(
        raw=raw,
        category='numerico',
        length=total,
        integer_digits=int_digits,
        decimal_digits=dec_digits,
        signed=signed,
        usage=usage,
    )


# ---------------------------------------------------------------------------
# Parser de linhas
# ---------------------------------------------------------------------------
_USAGE_RE = re.compile(
    r'\b(COMP-3|COMPUTATIONAL-3|COMP-4|COMPUTATIONAL-4|COMP-1|COMP-2|COMP|COMPUTATIONAL|BINARY|PACKED-DECIMAL|DISPLAY)\b',
    re.IGNORECASE,
)
_OCCURS_RE = re.compile(r'\bOCCURS\s+(\d+)', re.IGNORECASE)
_REDEF_RE = re.compile(r'\bREDEFINES\s+([\w-]+)', re.IGNORECASE)
_VALUE_RE = re.compile(r"\bVALUE\s+(.+?)\.?$", re.IGNORECASE)
_PIC_RE = re.compile(r'\b(?:PICTURE|PIC)\s+([^\s.]+(?:\s+[^\s.]+)*?)(?=\s+(?:COMP|COMPUTATIONAL|BINARY|PACKED|DISPLAY|VALUE|OCCURS)|\.|$)', re.IGNORECASE)
_LEVEL_NAME_RE = re.compile(r'^\s*(\d\d)\s+([\w-]+)')


def _normalize_usage(text: str) -> str:
    m = _USAGE_RE.search(text)
    if not m:
        return 'DISPLAY'
    u = m.group(1).upper()
    mapping = {
        'COMPUTATIONAL-3': 'COMP-3', 'PACKED-DECIMAL': 'COMP-3',
        'COMPUTATIONAL-4': 'COMP-4', 'BINARY': 'COMP-4',
        'COMPUTATIONAL': 'COMP',
        'COMPUTATIONAL-1': 'COMP-1', 'COMPUTATIONAL-2': 'COMP-2',
    }
    return mapping.get(u, u)


def _clean_line(line: str) -> str:
    """Remove numero de sequencia (col 1-6) e comentarios; devolve area de codigo."""
    # Linha de comentario: '*' na coluna 7 (indice 6) ou linha iniciada por '*'
    stripped = line.rstrip('\n').rstrip('\r')
    if len(stripped) >= 7 and stripped[6] == '*':
        return ''
    if stripped.lstrip().startswith('*'):
        return ''
    # Remove marcador de sequencia estilo *GOT* no fim
    stripped = re.sub(r'\*\w+\*\s*$', '', stripped)
    return stripped


def parse_copybook(text: str) -> list:
    """Parseia o texto de um copybook e devolve lista de Field de nivel raiz,
    com filhos aninhados conforme os niveis COBOL."""
    # Junta continuacoes: uma "sentenca" COBOL vai ate encontrar '.'
    linhas = []
    buffer = ''
    for raw in text.splitlines():
        code = _clean_line(raw)
        if not code.strip():
            continue
        buffer += ' ' + code.strip()
        if '.' in code:
            # pode haver multiplas sentencas na mesma linha; split por '.'
            partes = buffer.split('.')
            for p in partes[:-1]:
                if p.strip():
                    linhas.append(p.strip() + '.')
            buffer = partes[-1]
    if buffer.strip():
        linhas.append(buffer.strip())

    campos_flat = []
    for sent in linhas:
        m = _LEVEL_NAME_RE.match(sent)
        if not m:
            continue
        level = int(m.group(1))
        name = m.group(2).upper()
        is_filler = name == 'FILLER'

        redefines = None
        rm = _REDEF_RE.search(sent)
        if rm:
            redefines = rm.group(1).upper()

        occurs = 0
        om = _OCCURS_RE.search(sent)
        if om:
            occurs = int(om.group(1))

        usage = _normalize_usage(sent)

        pic = None
        pm = _PIC_RE.search(sent)
        if pm:
            pic = parse_pic(pm.group(1), usage=usage)

        value = None
        if pic is not None:
            vm = _VALUE_RE.search(sent)
            if vm:
                value = vm.group(1).strip()

        nullable = name.endswith('-NUL')

        campos_flat.append(Field(
            level=level, name=name, pic=pic, occurs=occurs,
            redefines=redefines, value=value, nullable=nullable,
            is_filler=is_filler,
        ))

    return _aninhar(campos_flat)


def _aninhar(flat: list) -> list:
    """Transforma a lista plana (com niveis) em arvore por nivel COBOL."""
    raiz = []
    pilha = []  # lista de (level, Field)
    for f in flat:
        while pilha and pilha[-1][0] >= f.level:
            pilha.pop()
        if pilha:
            pilha[-1][1].children.append(f)
        else:
            raiz.append(f)
        pilha.append((f.level, f))
    return raiz


def iter_elementary(campos: list):
    """Percorre a arvore e devolve (caminho_de_grupos, campo_elementar).

    Propaga nullable: se qualquer grupo ancestral termina em -NUL (convencao
    da conversao DMS->DB2 para colunas nullable), o campo elementar herda
    nullable=True.
    """
    def _walk(nodes, trilha):
        for n in nodes:
            if n.children:
                yield from _walk(n.children, trilha + [n])
            elif n.is_elementary and not n.is_filler:
                if not n.nullable and any(g.name.endswith('-NUL') for g in trilha):
                    n.nullable = True
                yield trilha, n
    yield from _walk(campos, [])


def parse_file(path) -> list:
    from pathlib import Path
    p = Path(path)
    return parse_copybook(p.read_text(encoding='latin-1', errors='ignore'))
