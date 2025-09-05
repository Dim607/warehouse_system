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
        return ", ".join(map(str, [
            self.id,
            self.username,
            self.password
        ]))


    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"Admin({attrs})"


    def to_dict(self) -> dict:
        return {
            "id":       self.id,
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        # id can be None so dont include it in the attr list
        attributes = ["username", "password"]

        for attr in attributes:
            if data.get(attr) is None:
                raise Exception(f"Attribute {attr} cannot be None")

        return cls (
            id       = data.get("id"),
            username = data.get("username"),
            password = data.get("password")
        )
