from typing import Any, List, Optional
from pymongo import ASCENDING, DESCENDING
from pymongo.database import Collection
from pymongo.results import InsertOneResult
from app.model.product import Product
from app.model.unit import Unit
from app.repositories.unit_repository import UnitRepository


class ProductRepository:
    product_collection: Collection
    unit_collection: Collection
    unit_repository: UnitRepository

    def __init__(self, product_collection: Collection, unit_collection: Collection, unit_repository: UnitRepository):
        self.product_collection = product_collection
        self.unit_collection    = unit_collection
        self.unit_repository    = unit_repository


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


    def insert_product(
        self,
        id: Optional[str],
        name: str,
        quantity: int,
        sold_quantity: int,
        weight: float,
        volume: float,
        category: str,
        purchase_price: float,
        selling_price: float,
        manufacturer: str,
        unit_gain: float,
        unit_id: str | None = None,
    ) -> List[InsertOneResult]:
        """
        Inserts a product to the database

        The product defined by the method's arguments is added to the unit identified by `unit_id`,
        if `unit_id is not None. If `unit_id` is None then the product is added to all units

        Args:
            id (str | None): The product ID. Can be None if not yet assigned.
            name (str): The name of the product.
            quantity (int): The number of items of the product to insert in the unit.
            sold_quantity (int): The number of items of the product sold from the unit.
            weight (float): The weight of one item of the product.
            volume (float): The volume of one item of the product.
            category (str): The category of the product (e.g., "Electronics", "Clothing").
            purchase_price (float): The cost price of one item of the product.
            selling_price (float): The selling price of one item of the product.
            manufacturer (str): The product manufacturer.
            unit_gain (float): The total gain or loss of the product in this unit.
            unit_id (str | None): The ID of the unit where the product will be inserted.
            If `unit_id` is None then the product is added to all the units

        Returns:
            List[pymongo.results.InsertOneResult]: A list with the result of the database insertion to one or all units

        Raises:
            ValueError: If the `unit_id` is specified but no unit is found with that ID
        """

        if unit_id is not None:
            if self._does_product_fit_in_unit(unit_id, int(quantity), float(volume)):
                return []

            result = self._insert_product_to_unit(
                id,
                name,
                quantity,
                sold_quantity,
                weight,
                volume,
                category,
                purchase_price,
                selling_price,
                manufacturer,
                unit_gain,
                unit_id,
            )
            return [result]

        result = self._insert_product_to_all_units(
            id,
            name,
            weight,
            volume,
            category,
            purchase_price,
            selling_price,
            manufacturer,
        )
        return result


    def _insert_product_to_unit(
        self,
        id: Optional[str],
        name: str,
        quantity: int,
        sold_quantity: int,
        weight: float,
        volume: float,
        category: str,
        purchase_price: float,
        selling_price: float,
        manufacturer: str,
        unit_gain: float,
        unit_id: str
    ) -> InsertOneResult:
        """
        Insert a product into a specific unit.

        Creates a Product instance and inserts it into the product collection 
        for the unit identified by `unit_id`.

        Args:
            id (str | None): The product ID. Can be None if not yet assigned.
            name (str): The name of the product.
            quantity (int): The number of items of the product to insert in the unit.
            sold_quantity (int): The number of items of the product sold from the unit.
            weight (float): The weight of one item of the product.
            volume (float): The volume of one item of the product.
            category (str): The category of the product (e.g., "Electronics", "Clothing").
            purchase_price (float): The cost price of one item of the product.
            selling_price (float): The selling price of one item of the product.
            manufacturer (str): The product manufacturer.
            unit_gain (float): The total gain or loss of the product in this unit.
            unit_id (str): The ID of the unit where the product will be inserted.

        Returns:
            pymongo.results.InsertOneResult: The result of the database insertion.

        Raises:
            ValueError:
            - If no unit with the given `unit_id` exists.
            - If any of the neccesary Product fields are missing when creating a Product instance
              from a dictionary
        """
        product: Product
        unit: Optional[Unit]
        prod_dict: dict

        unit = self.unit_repository.get_unit_by_id(unit_id)

        if unit is None:
            raise ValueError(f"Unit with id={unit_id} does not exist.")

        try:
            product = Product.from_dict(
                {
                    "id":             id,
                    "name":           name,
                    "quantity":       int(quantity),
                    "sold_quantity":  int(sold_quantity),
                    "weight":         float(weight),
                    "volume":         float(volume),
                    "category":       category,
                    "purchase_price": float(purchase_price),
                    "selling_price":  float(selling_price),
                    "manufacturer":   manufacturer,
                    "unit_gain":      float(unit_gain),
                }
            )
        except Exception as e:
            raise ValueError(f"Invalid product format") from e

        prod_dict = product.to_dict()
        prod_dict["unit_id"] = unit_id

        result = self.product_collection.insert_one(prod_dict)

        return result


    def _insert_product_to_all_units(
        self,
        id: Optional[str],
        name: str,
        weight: float,
        volume: float,
        category: str,
        purchase_price: float,
        selling_price: float,
        manufacturer: str,
    ) -> List[InsertOneResult]:
        """
        Insert a new product into all units.

        This method creates a Product with default values for quantity, sold_quantity,
        and unit_gain (all set to 0), then inserts it into the product collection for
        each unit in the system. A separate document is created for each unit.

        Args:
            id (str | None): The product ID. Can be None if not yet assigned.
            name (str): The name of the product.
            weight (float): The weight of one item of the product.
            volume (float): The volume of one item of the product.
            category (str): The category of the product (e.g., "Electronics", "Clothing").
            purchase_price (float): The cost price of one item of the product.
            selling_price (float): The selling price of one item of the product.
            manufacturer (str): The product manufacturer.

        Returns:
            List[pymongo.results.InsertOneResult]: A list of insertion results, one for each unit.

        Raises:
            ValueError: If any of the neccesary Product fields are missing when creating a Product instance
            from a dictionary
        """

        product: Product
        results: List[InsertOneResult] = []
        prod_dict: dict

        # add product to all units with quantity, sold_quantity, unit_gain all set to 0
        try:
            product = Product.from_dict(
                {
                    "id":             id,
                    "name":           name,
                    "quantity":       0,
                    "sold_quantity":  0,
                    "weight":         weight,
                    "volume":         volume,
                    "category":       category,
                    "purchase_price": purchase_price,
                    "selling_price":  selling_price,
                    "manufacturer":   manufacturer,
                    "unit_gain":      0,
                }
            )
        except Exception as e:
            raise ValueError(f"Invalid product format") from e

        prod_dict = product.to_dict()

        # get all units and unit ids
        unit_ids = self.unit_repository.get_all_units_ids()

        """ TODO maybe keep a list the product for each unit and add them all together """

        # insert a product to each unit by inserting it
        # multiple times to the product collection
        # but with different unit_id each time
        for unit_id in unit_ids:
            prod_dict["unit_id"] = unit_id
            result = self.product_collection.insert_one(prod_dict)
            results.append(result)

        return results


    def _does_product_fit_in_unit(self, unit_id: str, product_quantity: int, product_volume: float) -> bool:
        """
        Checks if a product can fit in the unit that is associated by `unit_id`

        This method gets the total volume of the unit associated by `unit_id`.
        It then gets information about how much storage each product of the unit takes up
        and subtracts it from the total volume.
        If the remainder is enough to store the product with `product_quantity` and `product_volume`
        the product can be placed inside the unit.

        Args:
        unit_id (str): The ID of the unit to check if a product fits in it
        product_quantity (int): The number of items of the product to insert in the unit.
        product_volume (float): The volume of one item of the product to insert to the unit.

        Returns:
            bool: True if there is space in the unit for the product, False otherwise

        Raises:
            ValueError: If no unit with the given `unit_id` exists
        """
        free_space: float
        used_space: float
        unit: Optional[Unit] = self.unit_repository.get_unit_by_id(unit_id)

        # no unit with unit_id was found
        if unit is None:
            raise ValueError(f"Unit with id={unit_id} does not exist.")

        # get storage information for all the products in the unit
        products = self.product_collection.find(
            {"unit_id": unit_id},
            projection={"quantity": 1, "volume": 1}
        )

        used_space = sum(p["quantity"] * p["volume"] for p in products)
        free_space = float(unit.volume) - used_space

        return free_space >= product_quantity * product_volume


    def buy_product(
        self,
        product_id: str,
        purchased_quantity: int,
        item_purchase_price: float,
    ) -> Product:
        """
        Buy a product and update it to the database

        This method fetches the database for the product identified by `product_id`.
        It then updates the unit_gain (balance) and the quantity for the product
        based on the `purchased_quantity` and the `purchase_price`

        Args:
            product_id (str): The id of the product to buy.
            purchased_quantity (int): The quantity of items of the product to be purchased.
            item_purchase_price (float): The price for each item of the product to be purchsed.

        Returns:
            Product: The updated product

        Raises:
            ValueError:
                - If no product exists with the given `product_id`
                - If the product could not be updated
        """
        loss: float
        buy_result: Any
        product: Optional[Product] = self.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with id={product_id} does not exist.")

        # loss MUST BE NEGATIVE because of $inc in the following query
        loss = - (item_purchase_price * purchased_quantity)

        # update the product and return the updated document
        buy_result = self.product_collection.find_one_and_update(
            {"id": product_id},
            {"$inc": {
                "quantity": purchased_quantity,
                "unit_gain": loss
            }},
            return_document=True
        )

        if buy_result is None:
            raise ValueError(f"Failed to update product with id={product_id}")

        return Product.from_dict(buy_result)


