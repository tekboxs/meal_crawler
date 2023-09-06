import logging
from datetime import datetime

import undetected_chromedriver

from MealLinkGetter import SEARCH_ENGINE, DOWNLOAD_DELAY, TIME_OUT
from MealLinkGetter.extract_image import extract_image_url_from_html, extract_image_url_from_script
from MealLinkGetter.search_by_name import get_script_from_page_by_name
from product_model import ProductModel


# dont thread this
def get_image_src_by_name(product_list: list[ProductModel]) -> list[ProductModel]:
    driver = undetected_chromedriver.Chrome(headless=True)
    result_list = product_list.copy()
    start = datetime.now()
    logging.info(f'Starting images link getter: {start} total itens = {len(product_list)}')
    for index, product in enumerate(product_list):
        link = get_script_from_page_by_name(SEARCH_ENGINE, product.descricao, TIME_OUT, driver)
        result_list[index].link = link

    driver.quit()
    logging.info(f'Finished images link getter total time: {datetime.now() - start}')

    return result_list


def get_image_src_by_name_old(product: ProductModel) -> ProductModel:
    image_html_raw = get_html_by_name(SEARCH_ENGINE, product.descricao, DOWNLOAD_DELAY)
    product.link = extract_image_url_from_html(image_html_raw)
    if product.link is None:
        logging.info(f'product: {product.id} CANT extract src')
    return product
