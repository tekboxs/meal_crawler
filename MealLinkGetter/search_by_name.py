import logging
import re
from typing import Mapping

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from time import sleep

import meal_error_logger
from MealLinkGetter import USER_AGENT, ERROR_LOG_FILE
from meal_error_logger import log_error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# def make_http_request(url: str, headers: Mapping[str, str | bytes] | None, delay):
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         sleep(delay)
#         return response.text
#     except RequestException as e:
#         print(f"Error while making the HTTP request: {e}")
#         log_error(ERROR_LOG_FILE, str(e))
#         return None
#
#
# def get_html_by_name(base_url: str, query: str, download_delay: int) -> str | None:
#     try:
#         complete_query = f'?q={quote_plus(query)}&tbm=isch'
#         headers = {"User-Agent": USER_AGENT}
#         html_content = make_http_request(base_url + complete_query, headers, download_delay)
#         if html_content is not None:
#             return html_content
#         else:
#             logging.info(f'{query} has not image!')
#             return None
#     except Exception as e:
#         print(f"{query} Error while parsing the HTML content: {e}")
#         log_error(ERROR_LOG_FILE, query + str(e))
#         return None


def get_script_from_page_by_name(base_url: str, query: str, time_out: int, driver):
    try:
        driver.get(base_url + f'?q={query}&tbm=isch')
        wait = WebDriverWait(driver, time_out)
        script_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "script")))
        image_url_pattern = r"https:[^\s]+?\.(?:jpg|png)[^\s]+?"

        image_urls = []
        for script_element in script_elements:
            try:
                script_content = script_element.get_attribute("innerHTML")
                urls_found = re.findall(image_url_pattern, script_content)
                image_urls.extend(urls_found)

            except Exception:
                pass

        for url in image_urls:
            x = (str(url).split('https://'))
            if len(x) >= 3:
                return 'https://' + x[2].rstrip(r'["?]')


    except Exception as e:
        print(f"Erro ao conectar a {query}")
        meal_error_logger.log_error(ERROR_LOG_FILE, f'{query} {e}')
        return None
