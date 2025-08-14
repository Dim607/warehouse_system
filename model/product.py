from __future__ import annotations  # for pyright typechecking
import uuid


"""
TODO
- Maybe add functions: is_xfield_valid()
"""

class Product:


    def __init__(
        self,
        id: str,
        name: str,
        quantity: float,  # maybe int
        weight: float,
        volume: float,
        category: str,  # TODO maybe add as collection to db
        purchase_price: float,
        selling_price: float,
        manufacturer: str,
        unit_gain: float,
    ):
        self.id: str               = id if id is not None else str(uuid.uuid4())
        self.name:str              = name 
        self.quantity:float        = quantity
        self.weight:float          = weight
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
                {self.quantity}, {self.weight}, \
                {self.volume}, {self.category}, \
                {self.purchase_price}, {self.selling_price}, \
                {self.manufacturer}, {self.unit_gain}"

    def __repr__(self):
        return f"Product('{self.id}', '{self.name}', \
                        '{self.quantity}', '{self.weight}', \
                        '{self.volume}', '{self.category}', \
                        '{self.purchase_price}', '{self.selling_price}', \
                        '{self.manufacturer}', '{self.unit_gain}',)"

    def to_dict(self):
        return {
            "id":               self.id,
            "name":             self.name,
            "quantity":         self.quantity,
            "weight":           self.weight,
            "volume":           self.volume,
            "category":         self.category,
            "purchase_price":   self.purchase_price,
            "selling_price":    self.selling_price,
            "manufacturer":     self.manufacturer,
            "unit_gain":        self.unit_gain,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id"),
            data.get("name"),
            data.get("quantity"),
            data.get("weight"),
            data.get("volume"),
            data.get("category"),
            data.get("purchase_price"),
            data.get("selling_price"),
            data.get("manufacturer"),
            data.get("unit_gain"),
        )
