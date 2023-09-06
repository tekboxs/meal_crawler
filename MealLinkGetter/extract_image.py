import logging
import re

from bs4 import BeautifulSoup


# def extract_image_url_from_html(html_text: str) -> str | None:
#     soup = BeautifulSoup(html_text, "html.parser")
#
#     for img in soup.find_all("img"):
#         link = img.get("src")
#         if link and not str(link).startswith('/images'):
#             return img.get("src")
#     return None





def extract_image_url_from_script(image_urls) -> str | None:
    if image_urls is None:
        return None
    for url in image_urls:
        x = (str(url).split('https://'))
        if len(x) >= 3:
            print(x[2].rstrip(r'["?]'))
            return 'https://' + (x[2].rstrip(r'["?]'))
