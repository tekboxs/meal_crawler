import cv2

from product_model import ProductModel


def save_image_by_product(product: ProductModel, save_pattern: str, directory: str) -> None:
    filename = save_pattern.format(id=product.id)
    cv2.imwrite(directory + filename, product.processed_image)
