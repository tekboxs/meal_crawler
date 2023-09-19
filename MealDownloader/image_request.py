import codecs
from time import sleep

import requests

from MealDownloader import logging, ERROR_LOG_FILE
from meal_error_logger import log_error
from product_model import ProductModel

import html


def execute_request(product: ProductModel, download_delay: int) -> ProductModel:
    try:
        if product.link is None:
            # logging.error(f"Product WITHOUT link {product.id} {product.descricao}")
            log_error(ERROR_LOG_FILE, f'{product.id} {product.descricao} - No image')
            return product

        response = requests.get(codecs.unicode_escape_decode(product.link)[0], timeout=30)

        if response.status_code == 200:
            product.image_bytes = response.content
            sleep(download_delay)
        else:
            # logging.error(f"Error on {product.id} {product.link} {response.status_code}")
            log_error(ERROR_LOG_FILE, str(product.id) + str(response.status_code))
    except Exception as e:
        # logging.error(f'Error on {product.id} {product.link} {product.descricao}')
        log_error(ERROR_LOG_FILE, f'{product.id} {product.descricao}- {product.link} {str(e)}')

    return product
