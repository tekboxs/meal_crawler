class ProductModel:
    def __init__(self, json: dict):
        self.descricao = json["descricao"]
        self.id = json["id"]
        self.link = json["link"]
        self.image_bytes = json["image_bytes"]
        self.processed_image = json["processed_image"]

