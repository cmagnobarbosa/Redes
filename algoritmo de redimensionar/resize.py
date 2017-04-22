from PIL import Image
from resizeimage import resizeimage
import glob
import os
"""
Script Simples para redefinir o tamanho de imagens.
"""
path = "imagens/"
cont = 0
for filename in os.listdir(path):
    if (".png") in filename:
        filename = path + filename
        cont =cont +1
        print cont," Convertendo ",filename
        #save_name= filename.split(".")[0]+"_new"+".png"
        with open(filename, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [172, 250])
                cover.save(filename, image.format)
print "Todas as imagens foram convertidas"
