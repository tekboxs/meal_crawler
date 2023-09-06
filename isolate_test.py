from MealDownloader.downloader import process_link_by_product
from MealLinkGetter.linker import get_image_src_by_name
from product_model import ProductModel

results = get_image_src_by_name(
    [ProductModel(
        json={
            "descricao": "JURUBEBA PRECIOSA 50ML",
            "id": 1,
            "image_bytes": None,
            "processed_image": None,
            "link": None
        }
    ),
        ProductModel(
            json={
                "descricao": "APERITIVO RAIZ AMARGA TORPEDO 970ML",
                "id": 2,
                "image_bytes": None,
                "processed_image": None,
                "link": None
            }
        ),
ProductModel(
            json={
                "descricao": "TAMPICO FRUTAS CITRICAS 450ML",
                "id": 3,
                "image_bytes": None,
                "processed_image": None,
                "link": None
            }
        )
    ]
)
for item in results:
    process_link_by_product(
        item
    )
