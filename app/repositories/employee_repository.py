from pymongo.database import Collection
from app.model.employee import Employee


"""
Avoid Singleton pattern, use Dependency Injection
This makes testing quicker
"""
class EmployeeRepository:
    employee_collection: Collection

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
    def get_employee(self, username: str, password: str, unit_id: str) -> Employee | None:
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


    # change the password of the employee with the corresponding id
    def change_password(self, id: str, password: str) -> bool:
        result = self.employee_collection.find_one_and_update(
            {"id": id},
            {"$set": {"password": password}}
        )
        if result is None:
            return False

        return True
