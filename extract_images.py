import os
import shutil

import MealDataBaseReader
from MealDataBaseReader.connector import db_connector


def extract_from_folders():
    pasta_destino = "C:/Users/Administrator/PycharmProjects/pythonProject/imagem_produtos"
    pasta_origem = pasta_destino

    extensoes_imagem = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    for pasta_raiz, subpastas, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            if any(arquivo.endswith(extensao) for extensao in extensoes_imagem):
                caminho_arquivo_origem = os.path.join(pasta_raiz, arquivo)
                caminho_arquivo_destino = os.path.join(pasta_destino, arquivo)

                shutil.copy2(caminho_arquivo_origem, caminho_arquivo_destino)

    print("Arquivos de imagem copiados com sucesso!")

