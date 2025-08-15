from  __future__ import annotations # for pyright typechecking
import uuid


class Employee:
    def __init__(
        self,
        id: str | None,
        name: str,
        surname: str,
        username: str,
        password: str,
        unit_id: str,
        unit_name: str,
    ):
        self.id: str | None = id if id is not None else str(uuid.uuid4())
        self.name: str      = name
        self.surname: str   = surname
        self.username: str  = username
        self.password: str  = password
        self.unit_id: str   = unit_id
        self.unit_name: str = unit_name


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
        return cls(
            data.get("id"),
            data.get("name"),
            data.get("surname"),
            data.get("username"),
            data.get("password"),
            data.get("unit_id"),
            data.get("unit_name"),
        )


    def change_password(self, new_password: str) -> bool:
        if self.password == new_password:
            return False
        self.password = new_password
        return True
