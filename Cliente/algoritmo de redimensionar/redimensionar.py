from PIL import Image
from resizeimage import resizeimage
import sys
"""
Script Simples para redefinir o tamanho de imagens.
Carlos Magno
"""

imagem = sys.argv[1]
largura= sys.argv[2]
altura = sys.argv[3]
print largura,altura
size = [int(largura),int(altura)]
print "imagem",imagem,"Tamanho:",largura,altura

with open(imagem, 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, size)
        cover.save(imagem, image.format)
print "O tamanho da imagem ",imagem,"foi ajustado para ",largura," x ",altura
