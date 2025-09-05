from typing import Optional
import uuid


class Unit:
    id: str
    name: str
    volume: float

    def __init__(self, id: Optional[str], name: str, volume: float):
        self.id: str       = id if id is not None else str(uuid.uuid4())
        self.name: str     = name
        self.volume: float = volume

    def __str__(self) -> str:
        return ", ".join(map(str, [
            self.id,
            self.name,
            self.volume
        ]))


    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"Unit({attrs})"


    def to_dict(self) -> dict:
        """
        Return the product as a dict
        """
        return {
            "id":     self.id,
            "name":   self.name,
            "volume": self.volume
        }


    @classmethod
    def from_dict(cls, data):
        """
        Get a unit object from a dictionary

        Can raise an exception if any of the attributes `name` or `volume` are missing

        :param data: A dictionary that has the unit's attributes as keys
        """
        # id can be None so dont include it in the attr list
        attributes = ["name", "volume"]

        for attr in attributes:
            if data.get(attr) is None:
                raise Exception(f"Attribute {attr} cannot be None")

        unit = cls(
            data.get("id"),
            data.get("name"),
            data.get("volume")
        )

        return unit 


    def add_product(self):
        pass
