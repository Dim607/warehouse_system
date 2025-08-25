from  __future__ import annotations # for pyright typechecking
from typing import Optional
from app.model.product import Product
from app.model.unit import Unit
import uuid


class Admin:

    def __init__(
        self,
        id: Optional[str],
        username: str,
        password: str,
    ):
        self.id: Optional[str] = id if id is not None else str(uuid.uuid4())
        self.username: str     = username
        self.password: str     = password

    def __eq__(self, other: Admin) -> bool:
        return self.id == other.id


    def __str__(self) -> str:
        return f"{self.id}, {self.username}, {self.password}"


    def __repr__(self) -> str:
        return f"Admin('{self.id}', '{self.username}', '{self.password}')"


    def to_dict(self) -> dict:
        return {
            "id":       self.id,
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        attributes = ["id", "username", "password"]


        for attr in attributes:
            if data.get(attr) is None:
                raise Exception(f"Attribute {attr} cannot be None")

        return cls (
            id       = data.get("id"),
            username = data.get("username"),
            password = data.get("password")
        )

    
    def add_product(
        self,
        product_id: Optional[str],
        product_name: str,
        product_quantity: int,
        product_sold_quantity: int,
        product_weight: float,
        product_volume: float,
        product_category: str,
        product_purchase_price: float,
        product_selling_price: float,
        product_manufacturer: str,
        product_unit_gain: float,
    ):
        product = Product(
            id = product_id,
            name = product_name,
            quantity = product_quantity,
            sold_quantity = product_sold_quantity,
            weight = product_weight,
            volume = product_volume,
            category = product_category,
            purchase_price = product_purchase_price,
            selling_price = product_selling_price,
            manufacturer = product_manufacturer,
            unit_gain = product_unit_gain,
        )
        return product


    def create_unit(self):
        pass


    # TODO delete
    # def create_supervisor(self, name: str, surname: str, username: str, password: str, unit_id: str, unit_name:str ) -> Supervisor:
    #     supervisor = Supervisor(
    #         id        = None,
    #         name      = name,
    #         surname   = surname,
    #         username  = username,
    #         password  = password,
    #         unit_id   = unit_id,
    #         unit_name = unit_name,
    #     )
    #     return supervisor










