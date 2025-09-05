from  __future__ import annotations # for pyright typechecking
from typing import Optional
import uuid


class Employee:
    id: Optional[str]
    name: str
    surname: str
    username: str
    password: str
    unit_id: str
    # unit_name is not saved in the database for each employee
    # because it can be found using unit_id
    # keep it here as a help field
    unit_name: str
    role: str = "employee"

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
        self.id           = id if id is not None else str(uuid.uuid4())
        self.name         = name
        self.surname      = surname
        self.username     = username
        self.password     = password
        self.unit_id      = unit_id
        self.unit_name    = unit_name


    def __eq__(self, other: Employee) -> bool:
        return self.id == other.id


    def __str__(self) -> str:
        return ", ".join(map(str, [
            self.id,
            self.name,
            self.surname,
            self.username,
            self.password,
            self.unit_id,
            self.unit_name,
        ]))


    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"Employee({attrs})"


    def to_dict(self) -> dict:
        return {
            "id":        self.id,
            "name":      self.name,
            "surname":   self.surname,
            "username":  self.username,
            "password":  self.password,
            "unit_id":   self.unit_id,
            "unit_name": self.unit_name,
            "role":      self.role
        }


    @classmethod
    def from_dict(cls, data):
        # id can be None so dont include it in the attr list
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
