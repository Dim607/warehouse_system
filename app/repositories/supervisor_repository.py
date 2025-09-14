from typing import List
from pymongo.database import Collection
from pymongo.results import InsertManyResult
from app.model.supervisor import Supervisor


class SupervisorRepository:
    user_collection: Collection

    def __init__(self, user_collection: Collection) -> None:
        self.user_collection = user_collection


    def insert_supervisors(self, supervisors: List[Supervisor]) -> InsertManyResult:
        """
        Inserts a supervisors to the database

        Removes the field `unit_name` from each supervisor in `supervisors`,
        only the `unit_id` is needed

        Args:
            supervisors (List[Supervisor]): A list with the supervisors to insert.

        Returns:
            pymongo.results.InsertManyResult: The result of the insertion.
        """
        return self.user_collection.insert_many([s.to_percistance_dict() for s in supervisors])
