import numpy as np
import cv2

from product_model import ProductModel


def resize_image(product: ProductModel, width=450, height=500) -> ProductModel:
    image_data = np.frombuffer(product.image_bytes, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    product.processed_image = cv2.resize(image,
                                         (width, height),
                                         interpolation=cv2.INTER_AREA
                                         )
    return product
