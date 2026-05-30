"""
Gera os rostos circulares usados no jogo (carlos_face.png / emerson_face.png)
a partir das fotos originais.

Uso:
    python tools/generate_faces.py

Requer Pillow:
    pip install Pillow

As fotos originais (carlos.png / emerson.jpeg) NÃO ficam no Git (.gitignore),
então precisam estar presentes localmente para rodar este script.

Para trocar um rosto: substitua a foto, ajuste o CROP correspondente abaixo
(esquerda, topo, direita, base em pixels) e rode de novo.
"""

import os
from PIL import Image, ImageDraw

# Pasta raiz do projeto (um nível acima de /tools)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (arquivo_origem, caixa_de_recorte, arquivo_saida)
# caixa = (esquerda, topo, direita, base)
JOBS = [
    ("carlos.png",   (180, 70, 180 + 350, 70 + 350),  "carlos_face.png"),
    ("emerson.jpeg", (210, 185, 210 + 170, 185 + 180), "emerson_face.png"),
]

SIZE = 256  # resolução final do rosto (quadrado)


def circle_face(src, box, out, size=SIZE):
    src_path = os.path.join(ROOT, src)
    out_path = os.path.join(ROOT, out)
    if not os.path.exists(src_path):
        print(f"  [PULADO] foto original não encontrada: {src}")
        return
    img = Image.open(src_path).convert("RGBA").crop(box).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    img.save(out_path)
    print(f"  [OK] {out}  <-  {src} {box}")


if __name__ == "__main__":
    print("Gerando rostos circulares...")
    for src, box, out in JOBS:
        circle_face(src, box, out)
    print("Concluído.")
