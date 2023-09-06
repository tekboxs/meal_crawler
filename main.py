import concurrent.futures
import logging
import time

from MealDataBaseReader.connector import db_connector
from MealDownloader.downloader import process_link_by_product
from MealLinkGetter.linker import get_image_src_by_name


def split_list_in_parts(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == "__main__":
    product_list = db_connector()

    logging.info(f'Db read, total itens {product_list}')

    chunk_size = 100
    chunks = list(split_list_in_parts(product_list, chunk_size))

    for idx, product_slice in enumerate(chunks):
        logging.info(f'Stating chunk number: {idx} ({idx * chunk_size})')
        product_with_link = get_image_src_by_name(product_slice)
        with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_size//2) as executor:
            executor.map(process_link_by_product, product_with_link)

        time.sleep(5)
