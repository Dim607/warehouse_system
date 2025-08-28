from typing import List, Optional
from pymongo.database import Collection
from app.model.employee import Employee


"""
Avoid Singleton pattern, use Dependency Injection
This makes testing quicker
"""
class EmployeeRepository:
    user_collection: Collection

    def __init__(self, employee_collection: Collection) -> None:
        self.user_collection = employee_collection


    def get_employee_by_id(self, id: str) -> Optional[Employee]:
        query = {"id": id, "role": "employee"}
        result = self.user_collection.find_one(query)

        if result is None:
            return None

        return Employee.from_dict(result)


    # Returns the employee whose username and password match the function parameters
    # If there is no employee it returns None
    # If an Employee object cannot be created from the data in the db an exception is raised
    def get_employee(self, username: str, password: str, unit_id: str) -> Optional[Employee]:
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


    def insert_employee(
        self,
        name: str,
        surname: str,
        username: str,
        password: str,
        unit_id: str,
        unit_name: str
    ):
        # create an employee obnect to validate fields
        employee = Employee.from_dict({
            "name":      name,
            "surname":   surname,
            "username":  username,
            "password":  password,
            "unit_id":   unit_id,
            "unit_name": unit_name,
            "role":      "employee"
        })

        # turn the previously created employee object into a dict and insert it to the user collection
        result = self.user_collection.insert_one(employee.to_dict())

        return {
            "acknowledged": result.acknowledged,
            "inserted_id": str(result.inserted_id)
        }


    def insert_employees(self, employees: List[Employee]):
        to_be_inserted = []
        for employee in employees:
            try:
                emp = Employee.from_dict(employee)
                to_be_inserted.append(emp.to_dict())
            except Exception as e:  # if one employee has wrong format stop
                raise ValueError(f"Invalid employee format: {employee}") from e

        result = self.user_collection.insert_many(to_be_inserted)

        return result

