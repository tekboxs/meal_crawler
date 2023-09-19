import concurrent.futures
import logging
import re
from datetime import datetime

from google_images_downloader import GoogleImagesDownloader

import meal_error_logger
from MealDataBaseReader.connector import db_connector
from MealDownloader.downloader import process_link_by_product
from MealLinkGetter.linker import get_image_src_by_name_single
from finalize_browsers import close_all_browsers
from product_model import ProductModel


def split_list_in_parts(lst: list[ProductModel], chunk_length: int):
    sorted_list = sorted(lst, key=lambda product: product.id)
    divided_list = [sorted_list[i:i + chunk_length] for i in range(0, len(sorted_list), chunk_length)]
    return divided_list


def clean_product_name(name: str) -> str:
    product_name = re.sub(r'((\w+[.:,]?)(\d+))|(\w+\.\b)', '', name)
    product_name = product_name.replace('-', '')
    product_name = product_name.replace('+', '')
    product_name = product_name.replace('#', '')
    product_name = product_name.replace('/', '')
    return product_name


def download_external(product: ProductModel):
    downloader = GoogleImagesDownloader(browser="chrome", show=False, debug=False,
                                        quiet=True, disable_safeui=False)  # Constructor with default values
    downloader.download(clean_product_name(product.descricao), limit=1, resize=(450, 500),
                        destination='C:/Users/Administrator/PycharmProjects/pythonProject/imagem_produtos')
    downloader.close()


def get_last_done_chunk_index(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                try:
                    last_value = int(last_line.split()[1])
                    return last_value
                except ValueError:
                    pass
    except FileNotFoundError:
        pass

    return -1


if __name__ == "__main__":
    product_list = db_connector()

    logging.info(f'Db read, total itens {len(product_list)}')

    chunk_size = 30
    chunks = list(split_list_in_parts(product_list, chunk_size))
    last_index = get_last_done_chunk_index('chunks_done.txt')
    for idx, product_slice in enumerate(chunks):
        if idx <= last_index:
            logging.info(f'Skipping chunk number: {idx + 1} (already done)')
            continue
        close_all_browsers()
        logging.info(f'Stating chunk number: {idx + 1} of {len(chunks)} ({(idx + 1) * chunk_size})')
        chunk_start = datetime.now()
        with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_size) as executor:
            product_with_link = executor.map(get_image_src_by_name_single, product_slice)
            executor.map(process_link_by_product, product_with_link)

        chunk_delta = datetime.now() - chunk_start
        meal_error_logger.log_error('chunks_done.txt', f'chunk {idx} done of {len(chunks)} ({(idx + 1) * chunk_size}')
        logging.info(f'chunk {idx + 1} finished in {chunk_delta}')
