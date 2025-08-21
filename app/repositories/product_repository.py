from typing import List
from pymongo.database import Collection
from app.model.product import Product


class ProductRepository:
    product_collection: Collection

    def __init__(self, product_collection: Collection):
        self.product_collection = product_collection

    def get_products(self) -> List[Product] | None:
        result = self.product_collection.find()
        if result is None:
            return None

        return [Product.from_dict(product) for product in result]
