import threading

import requests
import os
import cv2
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


def get_google_image_links(query, num_images=10):
    url = f"https://www.google.com/search?q={quote_plus(query)}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    image_links = []

    for img in soup.find_all("img"):
        link = img.get("src")
        if link:
            image_links.append(link)

    return image_links[:num_images]


def is_white_background(image_url):
    response = requests.get(image_url)
    image_data = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    mask = cv2.inRange(hsv_image, lower_white, upper_white)
    white_pixels = cv2.countNonZero(mask)
    total_pixels = mask.size
    white_percentage = white_pixels / total_pixels

    return white_percentage > 0.3


def download_images(image_links, download_folder):
    os.makedirs(download_folder, exist_ok=True)

    threads = []
    for idx, image_url in enumerate(image_links):
        thread = threading.Thread(target=download_image, args=(image_url, download_folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def download_image(image_links, download_folder):
    os.makedirs(download_folder, exist_ok=True)

    for idx, image_url in enumerate(image_links):
        try:
            if is_white_background(image_url):
                image_name = f"{idx + 1}.jpg"
                image_path = os.path.join(download_folder, image_name)
                with open(image_path, "wb") as f:
                    response = requests.get(image_url)
                    f.write(response.content)
                print(f"Downloaded image {image_name} with white background.")
                # break
        except Exception as e:
            print(f"Failed to download image {idx + 1}: {str(e)}")


if __name__ == "__main__":

    num_images_to_download = 10
    download_folder = "product_images"

    product_names = [
        "ARO P/ PNEU 3.25-8/350-8 C/ ROLAMENTO ROLETE 1",
        "MATA CUPIM ULTRA INSET 400ML/260G",
        "CARRINHO DE MAO CHAPA PR 45LT MASTER",
        "ESTOPA BRANCA POLIMENTO C/ 150G",
        "LUVA RASPA S/ REF 7CM",
        "JOELHO INTERNO 1/2",
        "FIBRA SINTETICA CAFE 10MM",
        "SOQUETE MAGNETICO 3/8",
        "SEPARADOR P/ARO DE CARRINHO",
        "SUPORTE DO EIXO P/ CARRINHO",
        "TINTA SPRAY ALTA TEMP ALUMINIO",
        "PULVERIZADOR 1,25L",
        "FIBRA SINTETICA CARAMELO 10MM",
        "FIBRA SINTETICA CHOCOLATE ESCURO 10MM",
        "CHAVE COMBINADA 7MM ROBUST",
        "FIBRA SINTETICA BANANEIRA 10MM",
        "VENTILADOR OSCIL VENTIR C/PE 60CM PT 127V",
        "PODAO TRAMONTINA  C/ CABO",
        "TRAVESSA CANELADA 600ML SORTIDO",
    ]
    image_links = []
    for product in product_names:
        image_links.append(get_google_image_links(product, num_images=num_images_to_download))
    download_images(image_links, download_folder)
