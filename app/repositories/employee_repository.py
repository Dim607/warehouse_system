# from pymongo import MongoClient
# from pymongo.database import Database, Collection
from pymongo.database import Collection
# from flask import current_app, request
# from typing import cast
# from app.custom_flask import CustomFlask
from app.model.employee import Employee
# from server import server


"""
Avoid Singleton pattern, use Dependency Injection
This makes testing quicker
"""
class EmployeeRepository:
    # _instance = None
    # db: Database
    # client: MongoClient
    employee_collection: Collection
    # cur_app: CustomFlask


    # @classmethod
    # def instance(cls):
    #     if cls._instance is None:
    #         cls._instance = cls.__new__(cls)
    #         # client = MongoClient(current_app.config["MONGO_HOST"], current_app.config["MONGO_PORT"])
    #         # cls._instance.db = client[""]
    #         # cls._instance.employee_collection = cls.db["employee"]
    #
    #         # cast current app to CustomFlask, 
    #         # otherwise db and employee_collection attributes cannot be used
    #         # without pyright complaining
    #         cur_app                           = cast(CustomFlask, current_app)
    #         cls._instance.db                  = cur_app.db
    #         cls._instance.employee_collection = cur_app.employee_collection
    #
    #         # cls._instance.db = server.db
    #         # cls._instance.employee_collection = server.employee_collection
    #     return cls._instance
    #
    # def __init__(self) -> None:
    #     raise RuntimeError('Call instance() instead')

    def __init__(self, employee_collection: Collection) -> None:
        self.employee_collection = employee_collection


    def get_employee_by_id(self, id: str) -> Employee | None:
        result = self.employee_collection.find({"id": id})
        if result is None:
            return None

        return Employee.from_dict(result)


    # Returns the employee whose username and password match the function parameters
    # If there is no employee it returns None
    # If an Employee object cannot be created from the data in the db an exception is raised
    def get_employee(self, username: str, password: str, unit_id) -> Employee | None:
        query = {
            "$and": [
                {"username": username},
                {"password": password},
                {"unit_id" : unit_id},
            ]
        }
        result = self.employee_collection.find_one(query)
        if result is None:
            return None

        return Employee.from_dict(result)

