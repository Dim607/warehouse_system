from typing import List, Optional
from pymongo import ASCENDING, DESCENDING
from pymongo.database import Collection
from pymongo.results import InsertManyResult, InsertOneResult
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


    def get_products_from_unit(self, unit_id: str):
        cursor = self.product_collection.find({"unit_id": unit_id})
        return [Product.from_dict(product) for product in cursor]


    def get_quantity_and_volume_by_unit(self, unit_id: str) -> List[dict]:
        cursor = self.product_collection.find(
            {"unit_id": unit_id},
            projection={"id": 1 ,"quantity": 1, "volume": 1}
        )
        return list(cursor)


    def buy_product(self, product_id: str, quantity: int , unit_gain: float) -> Product:
        """
        Increases the quantity and the unit_gain of the product identified by `product_id`

        Args:
            product_id (str): The id of the product to update.
            quantity (int): The amount of items of the product to add.
            unit_gain (float): The amount by which to increase the unit_gain of the product

        Returns:
            Product: The updated product

        Raises:
            ValueError:
                - If no  product was found with `product_id`
                - If the product is missing required order_fields
                (see Product.from_dict() for more details
        """
        result = self.product_collection.find_one_and_update(
            {"id": product_id},
            {"$inc": {
                "quantity": quantity,
                "unit_gain": unit_gain
            }},
            return_document=True
        )

        return Product.from_dict(result)


    def sell_product(self, product_id: str, sell_quantity: int, profit: float) -> Product:
        """
        Sell a product and update it in the database 

        This method decreases the product's quantity by `items_to_sell`
        and increases its `unit_gain` by the given `profit`.

        Args:
            product_id (str): The id of the product to sell.
            sell_quantity (int): The quantity of items of the product to be sold.
            profit (float): The profit from selling `sell_quantity` items

        Returns:
            Product: The updated product

        Raises:
            ValueError: 
                - If no  product was found with `product_id`
                - If the product is missing required order_fields
                (see Product.from_dict() for more details
        """
        sell_result: dict = self.product_collection.find_one_and_update(
            {
                "id": product_id,
                # are there enough items to sell
                "quantity": {"$gte": sell_quantity}
            },
            {
                "$inc": {
                    "quantity": -sell_quantity,  # subtract sold quantity
                    "unit_gain": profit,
                }
            },
            return_document=True,
        )

        return Product.from_dict(sell_result)


    def insert_product(self, product: Product) -> InsertOneResult:
        """
        Inserts a product to the database

        Args:
            product (Product): The product to insert

        Returns:
            pymongo.results.InsertOneResult: The result of the insertion
        """
        return self.product_collection.insert_one(product.to_dict())


    def insert_products(self, products: List[Product]) -> InsertManyResult:
        """
        Inserts a products to the database

        Args:
            products (List[Product]): A list with the products to insert

        Returns:
            pymongo.results.InsertOneResult: The result of the insertion
        """
        return self.product_collection.insert_many([p.to_dict() for p in products])


    """ FIXME do not raise value error """
    def search_products(
        self,
        order_field: Optional[str],
        order_type: Optional[str],
        name: Optional[str],
        id: Optional[str],
        start_index: Optional[int],
        end_index: Optional[int],
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
                cursor = cursor.sort(order_field, DESCENDING)
            else:
                cursor = cursor.sort(order_field, ASCENDING)

        return [Product.from_dict(product) for product in cursor]
