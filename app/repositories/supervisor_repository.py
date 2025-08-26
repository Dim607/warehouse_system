from typing import List
from pymongo.database import Collection
from app.model.supervisor import Supervisor


class SupervisorRepository:
    user_collection: Collection

    def __init__(self, user_collection: Collection) -> None:
        self.user_collection = user_collection


    def insert_supervisors(self, supervisors: List):
        to_be_inserted = []
        for supervisor in supervisors:
            sup = Supervisor.from_dict(supervisor)
            print(sup)
            try:
                to_be_inserted.append(sup.to_dict())
            except Exception as e:  # if one employee has wrong format stop
                raise ValueError(f"Invalid supervisor format: {supervisor}") from e

        result = self.user_collection.insert_many(to_be_inserted)

        return result
