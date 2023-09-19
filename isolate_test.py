import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import cv2
import shutil

import numpy as np
from PIL import Image

pasta_origem = r"C:\Users\Administrator\Desktop\test"

pasta_destino = r'C:\Users\Administrator\Desktop\post_images2'


def calculate_brightness(image):
    background = np.array([255, 255, 255])
    percent = (image == background).sum() / image.size
    if percent >= 0.3:
        return True
    else:
        return False


if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)


def processar_imagem(lista_arquivo):
    for arquivo in lista_arquivo:

        extensao = os.path.splitext(arquivo)[1].lower()

        imagem = cv2.imread(os.path.join(pasta_origem, arquivo))
        if not calculate_brightness(imagem):
            print(f'imagem pretaa {arquivo}')
            print(r"C:\Users\Administrator\Desktop\post_images2" + arquivo)

            os.chdir(r"C:\Users\Administrator\Desktop\post_images2")
            cv2.imwrite(arquivo, imagem)
        else:
            print(f'imagem branca {arquivo}')


imagens = [os.path.join(pasta_origem, arquivo) for arquivo in os.listdir(pasta_origem)]
tamanho_lote = 1
blocos_imagens = []
if len(imagens) > 0:
    blocos_imagens = [imagens[i:i + tamanho_lote] for i in range(0, len(imagens), tamanho_lote)]

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as executor:
        chunk_start = datetime.now()
        executor.map(processar_imagem, blocos_imagens)
        chunk_delta = datetime.now() - chunk_start

