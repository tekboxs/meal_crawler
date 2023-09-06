from time import sleep

import requests

from MealDownloader import logging, ERROR_LOG_FILE
from meal_error_logger import log_error
from product_model import ProductModel


def execute_request(product: ProductModel, download_delay: int) -> ProductModel:
    try:
        response = requests.get(product.link)

        if response.status_code == 200:
            product.image_bytes = response.content
            sleep(download_delay)
        else:
            logging.error(f"Error on {product.id} {product.link} {response.status_code}")
            log_error(ERROR_LOG_FILE, str(product.id) + str(response.status_code))
    except Exception as e:
        logging.error("Thread %s: Error while downloading image from %s: %s", 'links', product.id, str(e))
        log_error(ERROR_LOG_FILE, f'{product.id} - {product.link} {str(e)}')

    return product
