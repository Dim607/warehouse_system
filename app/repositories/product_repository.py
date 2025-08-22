from typing import List
import pymongo
from pymongo.database import Collection
from app.model.product import Product


class ProductRepository:
    product_collection: Collection

    def __init__(self, product_collection: Collection):
        self.product_collection = product_collection

    def get_product_by_id(self, id: str) -> Product | None:
        result = self.product_collection.find_one({"id": id})

        if result is None:
            return None

        return Product.from_dict(result)

    def get_products(self) -> List[Product]:
        result = self.product_collection.find()
        return [Product.from_dict(product) for product in result]

    def search_products(
        self,
        order_field: str | None,
        order_type: str | None,
        name: str | None,
        id: str | None,
        start_index: int | None,
        end_index: int | None,
    ) -> List[Product]:

        query: dict = {}
        cursor = []

        if name is not None:
            query["name"] = name

        if id is not None:
            query["id"] = id

        cursor = self.product_collection.find(query)

        if start_index is not None and end_index is not None:
            # are indexes valid?
            if (start_index > end_index) or (start_index < 0 or end_index < 0):
                raise ValueError

            # slash using start and end indexes
            limit: int = end_index - start_index
            # skip the first start_index results and show up to limit results
            cursor = cursor.skip(start_index).limit(limit)

        if order_field is not None:
            if order_type == "descending":
                cursor = cursor.sort(order_field, pymongo.DESCENDING)
            else:
                cursor = cursor.sort(order_field, pymongo.ASCENDING)

        return [Product.from_dict(product) for product in cursor]
