from typing import Any, List, Optional
from pymongo.results import InsertManyResult, InsertOneResult
from app.model.product import Product
from app.model.unit import Unit
from app.repositories.unit_repository import UnitRepository
from app.repositories.product_repository import ProductRepository


class ProductService():
    product_repo: ProductRepository
    unit_repository: UnitRepository

    def __init__(self, product_repo: ProductRepository, unit_repo: UnitRepository):
        self.product_repo = product_repo
        self.unit_repo = unit_repo


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
                    "unit_id":        unit_id,
                }
            )
        except Exception as e:
            raise ValueError(f"Invalid product format") from e

        result = self.product_repo.insert_product(product)

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
    ) -> InsertManyResult:
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
        result: InsertManyResult

        prod_dict = {
            "id": id,
            "name": name,
            "quantity": 0,
            "sold_quantity": 0,
            "weight": weight,
            "volume": volume,
            "category": category,
            "purchase_price": purchase_price,
            "selling_price": selling_price,
            "manufacturer": manufacturer,
            "unit_gain": 0,
        }

        # get all units and unit ids
        unit_ids = self.unit_repository.get_all_units_ids()

        insert_list = []

        for unit_id in unit_ids:
            prod_dict_copy = dict(prod_dict)
            prod_dict_copy["unit_id"] = unit_id
            try:
                product = Product.from_dict(prod_dict_copy)
            except Exception as e:
                raise ValueError(f"Invalid product format") from e
            insert_list.append(product)
        # insert a product to each unit by inserting it multiple times
        # but with different unit_id each time
        result = self.product_repo.insert_products(insert_list)

        return result


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
        products = self.product_repo.get_quantity_and_volume_by_unit(unit_id)

        used_space = sum(p["quantity"] * p["volume"] for p in products)
        free_space = float(unit.volume) - used_space

        return free_space >= product_quantity * product_volume


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
    ) -> InsertOneResult | InsertManyResult:
        """
        Inserts a product to the database

        The product defined by the method's arguments is added to the unit identified by `unit_id`,
        if `unit_id` is not None. If `unit_id` is None then the product is added to all units

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
            pymongo.results.InsertOneResult: If inserting to a single unit.
            pymongo.results.InsertManyResult: If inserting to all units.

        Raises:
            ValueError: 
                - If the `unit_id` is specified but no unit is found with that ID
                - If there is not enough space in the unit with `unit_id` to fit the product
        """

        if unit_id is not None:
            if not self._does_product_fit_in_unit(unit_id, int(quantity), float(volume)):
                raise ValueError(f"Product with id={id} does not fit in unit")

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
            return result

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


    def buy_product(
        self,
        product_id: str,
        purchased_quantity: int,
    ) -> Product:
        """
        Buy a product and update it to the database

        This method fetches the database for the product identified by `product_id`.
        It then decreases the unit_gain (balance) and increases the quantity of the product
        based on the `purchased_quantity`.

        Args:
            product_id (str): The id of the product to buy.
            purchased_quantity (int): The quantity of items of the product to be purchased.

        Returns:
            Product: The updated product

        Raises:
            ValueError:
                - If no product exists with the given `product_id`
                - If there is no space for the product in the unit it is in.
                - If the product could not be updated
        """
        unit_id: str
        loss: float
        product: Optional[Product] = self.product_repo.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with id={product_id} does not exist.")

        unit_id = product.unit_id

        if not self._does_product_fit_in_unit(unit_id, int(purchased_quantity), float(product.volume)):
            raise ValueError(f"Product with id={product_id} does not fit into unit with id={unit_id}")

        # loss MUST BE NEGATIVE because of $inc in the following query
        loss = - (product.purchase_price * purchased_quantity)

        # update the product and return the updated document
        try:
            updated_product = self.product_repo.buy_product(
                product_id, purchased_quantity, loss
            )
        except ValueError as e:
            raise ValueError(f"Could not buy product") from e

        return updated_product


    def sell_product(
        self,
        product_id: str,
        quantity_to_sell: int,
    ) -> Product:
        """
        Sell a product by validating and updating it.

        This service method:
        1. Checks that the product exists.
        2. Calculates the profit for the given quantity to sell.
        3. Calls repository to update the product.

        Args:
            product_id (str): The ID of the product to sell.
            quantity_to_sell (int): The number of items to sell.

        Returns:
            Product: The updated product object after the sale.

        Raises:
            ValueError: If
                - The product does not exist.
                - The quantity to sell exceeds the available stock.
                - The repository fails to update the product.
        """
        profit: float
        product: Optional[Product] = self.product_repo.get_product_by_id(product_id)

        if product is None:
            raise ValueError(f"Product with id={product_id} does not exist.")

        profit = (product.selling_price - product.purchase_price) * quantity_to_sell

        try:
            updated_product = self.product_repo.sell_product(product_id, quantity_to_sell, profit)
        except Exception as e:
            raise ValueError(f"Could not sell product") from e

        return updated_product
