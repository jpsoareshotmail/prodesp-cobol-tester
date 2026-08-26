"""Le o texto de arquivos .docx (sem libs externas) via o XML interno."""
import re
import sys
import zipfile
from pathlib import Path


def ler_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        # document.xml e sempre UTF-8 no formato .docx (OOXML)
        xml = z.read('word/document.xml').decode('utf-8')
    # Quebra de paragrafo -> nova linha
    xml = xml.replace('</w:p>', '\n')
    # Quebra de linha explicita
    xml = re.sub(r'<w:br[^/]*/>', '\n', xml)
    # Tabs
    xml = xml.replace('<w:tab/>', '\t')
    # Remove todas as tags, mantendo o texto de <w:t>
    texto = re.sub(r'<[^>]+>', '', xml)
    # Desescapa entidades comuns
    for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")]:
        texto = texto.replace(a, b)
    # Limpa linhas vazias excessivas
    linhas = [l.rstrip() for l in texto.splitlines()]
    out = []
    vazias = 0
    for l in linhas:
        if l.strip() == '':
            vazias += 1
            if vazias <= 1:
                out.append('')
        else:
            vazias = 0
            out.append(l)
    return '\n'.join(out).strip()


if __name__ == '__main__':
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('Roteiros de Teste')
    for f in sorted(pasta.glob('*.docx')):
        print('=' * 80)
        print('ARQUIVO:', f.name)
        print('=' * 80)
        print(ler_docx(f))
        print()
