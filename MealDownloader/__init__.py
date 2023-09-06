# responsible for download image with link

import logging

DEFAULT_DOWNLOAD_PATH = '/product_images'
ERROR_LOG_FILE = 'download_errors.txt'
FORMATTER = "%(asctime)s: %(message)s"

logging.basicConfig(format=FORMATTER, level=logging.INFO,
                    datefmt="%H:%M:%S")
