from typing import Optional
import uuid


class Unit:
    def __init__(self, id: Optional[str], name: str, volume: float):
        self.id: Optional[str] = id if id is not None else str(uuid.uuid4())
        self.name: str         = name
        self.volume: float     = volume

    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {self.volume}";


    def __repr__(self) -> str:
        return f"Unit('{self.id}', '{self.name}', '{self.volume}')";


    def to_dict(self) -> dict:
        return {
            "id":     self.id,
            "name":   self.name,
            "volume": self.volume
        }


    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id"),
            data.get("name"),
            data.get("volume")
        )

    def add_product(self):
        pass
