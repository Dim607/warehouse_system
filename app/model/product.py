from __future__ import annotations  # for pyright typechecking
import uuid
from typing import Optional
from operator import attrgetter


"""
TODO
- Maybe add functions: is_xfield_valid()
- Maybe add category as collection to db
"""

class Product:
    id: Optional[str]
    name: str
    quantity: int
    sold_quantity: int
    weight: float
    volume: float
    category: str
    purchase_price: float
    selling_price: float
    manufacturer: str
    unit_gain: float

    def __init__(
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
    ):
        self.id: Optional[str]     = id if id is not None else str(uuid.uuid4())
        self.name:str              = name 
        self.quantity: int         = quantity
        self.sold_quantity: int    = sold_quantity
        self.weight: float         = weight
        self.volume: float         = volume
        self.category: str         = category
        self.purchase_price: float = purchase_price
        self.selling_price: float  = selling_price
        self.manufacturer: str     = manufacturer
        self.unit_gain: float      = unit_gain


    def __eq__(self, other: Product) -> bool:
        return self.id == other.id

    def __str__(self):
        return f"{self.id}, {self.name}, \
                {self.quantity}, {self.sort_sold_quantity}, \
                {self.weight}, \
                {self.volume}, {self.category}, \
                {self.purchase_price}, {self.selling_price}, \
                {self.manufacturer}, {self.unit_gain}"

    def __repr__(self):
        return f"Product('{self.id}', '{self.name}', \
                        '{self.quantity}', '{self.sort_sold_quantity}', \
                        '{self.weight}', \
                        '{self.volume}', '{self.category}', \
                        '{self.purchase_price}', '{self.selling_price}', \
                        '{self.manufacturer}', '{self.unit_gain}',)"

    def to_dict(self):
        return {
            "id":             self.id,
            "name":           self.name,
            "quantity":       self.quantity,
            "sold_quantity":  self.sold_quantity,
            "weight":         self.weight,
            "volume":         self.volume,
            "category":       self.category,
            "purchase_price": self.purchase_price,
            "selling_price":  self.selling_price,
            "manufacturer":   self.manufacturer,
            "unit_gain":      self.unit_gain,
        }

    @classmethod
    def from_dict(cls, data):

        # id can be None so dont include it in the attr list
        attributes = [
            "name",
            "quantity",
            "sold_quantity",
            "weight",
            "volume",
            "category",
            "purchase_price",
            "selling_price",
            "manufacturer",
            "unit_gain"
        ]

        for attr in attributes:
            if data.get(attr) is None:
                raise Exception(f"Attribute {attr} cannot be None")

        product = cls(
            id             = data.get("id"),
            name           = data.get("name"),
            quantity       = data.get("quantity"),
            sold_quantity  = data.get("sold_quantity"),
            weight         = data.get("weight"),
            volume         = data.get("volume"),
            category       = data.get("category"),
            purchase_price = data.get("purchase_price"),
            selling_price  = data.get("selling_price"),
            manufacturer   = data.get("manufacturer"),
            unit_gain      = data.get("unit_gain"),
        )

        return product


    def sell_product(self, sold_product: int):
        self.sold_quantity = self.sold_quantity + sold_product
        self.quantity      = self.quantity - sold_product
        self.unit_gain     = self.selling_price * sold_product


    @staticmethod
    def sort_name(product_list: list[Product], reverse: bool):
        """
        Sorts in place based on product name
        if reverse = true -> sort in descending order
        """
        product_list.sort(key=attrgetter("name"), reverse=reverse)


    @staticmethod
    def sort_sold_quantity(product_list: list[Product], reverse: bool):
        """
        Sorts in place based on product sold quantity
        if reverse = true -> sort in descending order
        """
        product_list.sort(key=attrgetter("sold_quantity"), reverse=reverse)        
