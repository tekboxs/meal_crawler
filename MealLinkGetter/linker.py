import logging
import re
from datetime import datetime

import undetected_chromedriver
from selenium import webdriver

from MealLinkGetter import SEARCH_ENGINE, DOWNLOAD_DELAY, TIME_OUT
# from MealLinkGetter.extract_image import extract_image_url_from_script
from MealLinkGetter.search_by_name import get_script_from_page_by_name
from product_model import ProductModel


def get_image_src_by_name(product_list: list[ProductModel]) -> list[ProductModel]:
    driver = undetected_chromedriver.Chrome(headless=True)

    result_list = product_list.copy()
    start = datetime.now()
    for index, product in enumerate(product_list):
        link = get_script_from_page_by_name(SEARCH_ENGINE, product.descricao, TIME_OUT, driver)
        result_list[index].link = link

    driver.quit()
    logging.info(f'Finished images link getter total time: {datetime.now() - start}')

    return result_list


def clean_product_name(name: str) -> str:
    product_name = re.sub(r'((\w+[.:,]?)(\d+))|(\w+\.\b)', '', name)
    product_name = product_name.replace('-', '')
    product_name = product_name.replace('+', '')
    product_name = product_name.replace('#', '')
    product_name = product_name.replace('/', '')
    return product_name


def get_image_src_by_name_single(product: ProductModel) -> ProductModel:
    options = webdriver.ChromeOptions()

    options.add_argument("-headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    link = get_script_from_page_by_name(SEARCH_ENGINE, clean_product_name(product.descricao), TIME_OUT, driver)
    product.link = link
    driver.quit()
    # logging.info(f'Finished images link getter total time: {datetime.now() - start}')

    return product
