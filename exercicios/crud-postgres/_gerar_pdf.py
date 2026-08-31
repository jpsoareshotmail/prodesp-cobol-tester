"""
Gera ATIVIDADES_ESTAGIARIO.pdf a partir do markdown, usando reportlab.
Renderiza titulos, paragrafos, listas, tabelas e blocos de codigo.
"""
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, HRFlowable)

BASE = Path('exercicios/crud-postgres')
MD = BASE / 'ATIVIDADES_ESTAGIARIO.md'
PDF = BASE / 'ATIVIDADES_ESTAGIARIO.pdf'

styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#1A1A1A'), spaceAfter=10)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1A1A1A'), spaceBefore=14, spaceAfter=6)
H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11.5, textColor=colors.HexColor('#333333'), spaceBefore=8, spaceAfter=4)
BODY = ParagraphStyle('BODY', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=4)
BULLET = ParagraphStyle('BULLET', parent=BODY, leftIndent=14, bulletIndent=4)
CODE = ParagraphStyle('CODE', parent=styles['Code'], fontSize=8.5, leading=11,
                      textColor=colors.HexColor('#0A3D0A'), backColor=colors.HexColor('#F2F4F2'),
                      borderPadding=6, leftIndent=4, spaceBefore=4, spaceAfter=6)


def inline(t: str) -> str:
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<font face="Courier">\1</font>', t)
    return t


def build():
    linhas = MD.read_text(encoding='utf-8').splitlines()
    flow = []
    i = 0
    in_code = False
    code_buf = []
    while i < len(linhas):
        linha = linhas[i]

        if linha.strip().startswith('```'):
            if in_code:
                flow.append(Preformatted('\n'.join(code_buf), CODE))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(linha)
            i += 1
            continue

        # tabela
        if linha.strip().startswith('|') and i + 1 < len(linhas) and re.match(r'\s*\|[-\s|]+\|', linhas[i+1]):
            headers = [c.strip() for c in linha.strip().strip('|').split('|')]
            rows = [headers]
            j = i + 2
            while j < len(linhas) and linhas[j].strip().startswith('|'):
                rows.append([c.strip() for c in linhas[j].strip().strip('|').split('|')])
                j += 1
            data = [[Paragraph(inline(c), BODY) for c in r] for r in rows]
            t = Table(data, repeatRows=1, hAlign='LEFT')
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A1A1A')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7F8FA')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            flow.append(t)
            flow.append(Spacer(1, 6))
            i = j
            continue

        m = re.match(r'^(#{1,4})\s+(.*)', linha)
        if m:
            nivel = len(m.group(1))
            texto = inline(m.group(2))
            flow.append(Paragraph(texto, {1: H1, 2: H2, 3: H3}.get(nivel, H3)))
            i += 1
            continue

        if linha.strip() == '---':
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD')))
            flow.append(Spacer(1, 4))
            i += 1
            continue

        m = re.match(r'^(\s*)[-*]\s+(.*)', linha)
        if m:
            flow.append(Paragraph(inline(m.group(2)), BULLET, bulletText='\u2022'))
            i += 1
            continue

        # citacao
        m = re.match(r'^>\s?(.*)', linha)
        if m:
            flow.append(Paragraph('<i>' + inline(m.group(1)) + '</i>', BODY))
            i += 1
            continue

        if linha.strip():
            flow.append(Paragraph(inline(linha.strip()), BODY))
        else:
            flow.append(Spacer(1, 4))
        i += 1

    doc = SimpleDocTemplate(str(PDF), pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.8*cm, bottomMargin=1.8*cm,
                            title='Atividades CRUD PostgreSQL')
    doc.build(flow)
    print('PDF gerado:', PDF)


if __name__ == '__main__':
    build()
