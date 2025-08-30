from typing import List
from pymongo.database import Collection
from app.model.unit import Unit


"""
Avoid Singleton pattern, use Dependency Injection
This makes testing quicker
"""
class UnitRepository:
    unit_collection: Collection

    def __init__(self, unit_collection: Collection):
        self.unit_collection = unit_collection


    def get_all_units(self) -> List[Unit]:
        """
        Get all the stored units
        """
        result = self.unit_collection.find()
        return [Unit.from_dict(unit) for unit in result]


    def get_all_units_ids(self) -> List[str]:
        """
        Get the ids of all the stored units

        Returns the ids of all the stored units as a list of strings
        """
        cursor = self.unit_collection.find({}, projection={"id": 1, "_id": 0})
        # instead of returning a list like: [{id: 1}, {id: 2}...], return [1, 2, ...]
        return [unit.get("id") for unit in cursor if "id" in unit]


    def get_unit_by_id(self, id: str) -> Unit | None:
        """
        Get the unit with the specified id

        :param id: A string specifying the id of the unit to retrieve from the database
        """

        result = self.unit_collection.find_one({"id": id})

        if result is None:
            return None

        return Unit.from_dict(result)


    def insert_unit(
        self,
        id: str,
        name: str,
        volume: float
    ):
        """
        Insert a unit to the unit Collection
        :param id: string with the id of the unit to insert to the database
        :param name: string with the name of the unit
        :param volume: float with the total volume of the unit
        """
        unit = Unit.from_dict({
            "id":     id,
            "name":   name,
            "volume": volume
        })

        result = self.unit_collection.insert_one(unit.to_dict())

        return {
            "acknowledged": result.acknowledged,
            "inserted_id": str(result.inserted_id)
        }

    def insert_units(self, units: List[Unit]):
        """
        Insert multiple units to the unit Collection

        If any of the units are not valid `Unit` objects a ValueError exception is thrown

        :param units: A list containing all the units to be inserted
        """
        to_be_inserted = []
        for unit in units:
            try:
                emp = Unit.from_dict(unit)
                to_be_inserted.append(emp.to_dict())
            except Exception as e:  # if one employee has wrong format stop
                raise ValueError(f"Invalid unit format: {unit}") from e

        result = self.unit_collection.insert_many(to_be_inserted)

        return result
