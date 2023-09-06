from product_model import ProductModel
import pandas as pd


def data_frame_to_product_list(frame: pd.DataFrame) -> list[ProductModel]:
    product_models = []
    for index, row in frame.iterrows():
        json_data = {
            "descricao": row['description'],
            "id": row['id'],
            "link": None,
            "image_bytes": None,
            "processed_image": None
        }
        product = ProductModel(json_data)
        product_models.append(product)

    return product_models
