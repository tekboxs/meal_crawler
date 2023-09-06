from MealDownloader.proccess_image import resize_image
from MealDownloader.save_image import save_image_by_product
from product_model import ProductModel
from MealDownloader.image_request import execute_request


def process_link_by_product(product: ProductModel) -> None:
    products_with_bytes = execute_request(product, 1)
    products_complete = resize_image(products_with_bytes)
    save_image_by_product(products_complete,
                          save_pattern='Produto1_{id}.jpg',
                          directory='C:/Users/Administrator/Desktop/product_images/'
                          )
