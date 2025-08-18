from  __future__ import annotations # for pyright typechecking
from typing import Optional
import uuid


class Employee:
    def __init__(
        self,
        id: Optional[str],
        name: str,
        surname: str,
        username: str,
        password: str,
        unit_id: str,
        unit_name: str,
    ):
        self.id: Optional[str] = id if id is not None else str(uuid.uuid4())
        self.name: str         = name
        self.surname: str      = surname
        self.username: str     = username
        self.password: str     = password
        self.unit_id: str      = unit_id
        self.unit_name: str    = unit_name


    def __eq__(self, other: Employee) -> bool:
        return self.id == other.id


    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {self.surname}, {self.username}, {self.password}, {self.unit_id}, {self.unit_name}"

    
    def __repr__(self) -> str:
        return f"Employee('{self.id}', '{self.name}', '{self.surname}', '{self.username}', '{self.password}', '{self.unit_id}', '{self.unit_name}')"


    def to_dict(self) -> dict:
        return {
            "id":        self.id,
            "name":      self.name,
            "surname":   self.surname,
            "username":  self.username,
            "password":  self.password,
            "unit_id":   self.unit_id,
            "unit_name": self.unit_name,
        }


    @classmethod
    def from_dict(cls, data):
        attributes = ["name", "surname", "username", "password", "unit_id", "unit_name"]

        for attr in attributes:
            if data.get(attr) is None:
                raise Exception(f"Attribute {attr} cannot be None")

        employee = cls(
            id        = data.get("id"),
            name      = data.get("name"),
            surname   = data.get("surname"),
            username  = data.get("username"),
            password  = data.get("password"),
            unit_id   = data.get("unit_id"),
            unit_name = data.get("unit_name"),
        )
        return employee

    def change_password(self, new_password: str) -> bool:
        if self.password == new_password:
            return False
        self.password = new_password
        return True
