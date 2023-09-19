import numpy as np
import cv2

from product_model import ProductModel

import cv2
import numpy as np


def resize_image(product: ProductModel, width=375, height=500) -> ProductModel:
    image_data = np.frombuffer(product.image_bytes, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    width_ratio = width / image.shape[1]
    height_ratio = height / image.shape[0]

    scale_factor = min(width_ratio, height_ratio)

    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)

    product.processed_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    top_padding = (height - new_height) // 2
    bottom_padding = height - new_height - top_padding
    left_padding = (width - new_width) // 2
    right_padding = width - new_width - left_padding

    product.processed_image = cv2.copyMakeBorder(
        product.processed_image,
        top_padding,
        bottom_padding,
        left_padding,
        right_padding,
        cv2.BORDER_CONSTANT,
        value=(255, 255, 255)
    )

    return product
