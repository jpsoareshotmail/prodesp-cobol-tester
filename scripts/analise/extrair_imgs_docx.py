"""Extrai as imagens embutidas em arquivos .docx para uma pasta."""
import sys
import zipfile
from pathlib import Path


def extrair(docx: Path, destino: Path):
    destino.mkdir(parents=True, exist_ok=True)
    n = 0
    with zipfile.ZipFile(docx) as z:
        medias = sorted(x for x in z.namelist() if x.startswith('word/media/'))
        for m in medias:
            data = z.read(m)
            nome = Path(m).name
            (destino / nome).write_bytes(data)
            n += 1
    return n, medias


if __name__ == '__main__':
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('Roteiros de Teste')
    out_base = Path('_imgs_roteiros')
    for f in sorted(pasta.glob('*.docx')):
        destino = out_base / f.stem.strip()
        n, medias = extrair(f, destino)
        print(f'{f.name}: {n} imagens -> {destino}')
        for m in medias:
            print(f'    {m}')
