from pymongo.database import Collection
from app.model.employee import Employee
from app.model.supervisor import Supervisor
from app.model.admin import Admin


"""
Avoid Singleton pattern, use Dependency Injection
This makes testing quicker
"""
class EmployeeRepository:
    user_collection: Collection

    def __init__(self, employee_collection: Collection) -> None:
        self.user_collection = employee_collection

    def get_employee_by_id(self, id: str) -> Employee | None:
        query = {"id": id, "role": "employee"}
        result = self.user_collection.find_one(query)

        if result is None:
            return None

        return Employee.from_dict(result)


    # Returns the employee whose username and password match the function parameters
    # If there is no employee it returns None
    # If an Employee object cannot be created from the data in the db an exception is raised
    def get_employee(self, username: str, password: str, unit_id: str):
        query = {
            "$and": [
                {"username": username},
                {"password": password},
                {"unit_id":  unit_id},
                {"role":     "employee"}
            ]
        }

        result = self.user_collection.find_one(query)

        if result is None:
            return None

        return Employee.from_dict(result)
