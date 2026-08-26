"""
Extrai as imagens dos .docx dos roteiros para frontend/static/roteiros/<id>/
na ORDEM em que aparecem no documento, e gera um indice JSON.

As imagens sao servidas pelo Flask em /static/roteiros/<id>/NN.png
"""
import json
import re
import zipfile
from pathlib import Path

ROTEIROS_DIR = Path('Roteiros de Teste')
OUT_DIR = Path('frontend/static/roteiros')

# mapeia arquivo .docx -> id do roteiro (mesmo id de data/roteiros_teste.py)
MAP_ID = {
    'capital': 'capital',
    'interior': 'interior_litoral',
    'oficial': 'orgao_oficial',
}


def id_do_arquivo(nome: str) -> str:
    n = nome.lower()
    if 'capital' in n:
        return 'capital'
    if 'interior' in n or 'litoral' in n:
        return 'interior_litoral'
    if 'oficial' in n or 'rg' in n:  # orgao oficial (encoding do nome varia)
        return 'orgao_oficial'
    return None


def imagens_na_ordem(zf: zipfile.ZipFile) -> list:
    """Retorna os nomes de imagem na ordem em que sao referenciadas no documento."""
    doc = zf.read('word/document.xml').decode('utf-8', errors='ignore')
    rels = zf.read('word/_rels/document.xml.rels').decode('utf-8', errors='ignore')
    # rId -> target (media/imageN.png)
    rid_to_target = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    # ordem dos r:embed no documento
    ordem = re.findall(r'r:embed="([^"]+)"', doc)
    resultado = []
    for rid in ordem:
        tgt = rid_to_target.get(rid, '')
        if tgt.startswith('media/'):
            resultado.append('word/' + tgt)
    return resultado


def main():
    indice = {}
    for docx in sorted(ROTEIROS_DIR.glob('*.docx')):
        rid = id_do_arquivo(docx.name)
        if not rid:
            print('IGNORADO (id nao reconhecido):', docx.name)
            continue
        destino = OUT_DIR / rid
        destino.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(docx) as zf:
            ordem = imagens_na_ordem(zf)
            arquivos = []
            for i, media in enumerate(ordem, start=1):
                try:
                    data = zf.read(media)
                except KeyError:
                    continue
                nome = f'{i:02d}.png'
                (destino / nome).write_bytes(data)
                arquivos.append(f'/static/roteiros/{rid}/{nome}')
            indice[rid] = arquivos
        print(f'{docx.name} -> {rid}: {len(indice[rid])} imagens')

    idx_path = OUT_DIR / 'indice.json'
    idx_path.write_text(json.dumps(indice, indent=2), encoding='utf-8')
    print('Indice gerado:', idx_path)


if __name__ == '__main__':
    main()
