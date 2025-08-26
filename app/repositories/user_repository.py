from pymongo.database import Collection
from app.model.employee import Employee
from app.model.supervisor import Supervisor
from app.model.admin import Admin


"""
Avoid Singleton pattern, use Dependency Injection
This makes testing quicker
"""
class UserRepository:
    user_collection: Collection

    def __init__(self, user_collection: Collection) -> None:
        self.user_collection = user_collection


    def get_user_by_id(self, id: str) -> Employee | None:
        result = self.user_collection.find_one({"id": id})

        if result is None:
            return None

        return Employee.from_dict(result)


    # Returns the employee whose username and password match the function parameters
    # If there is no employee it returns None
    # If an Employee object cannot be created from the data in the db an exception is raised
    def get_user(self, username: str, password: str, unit_id: str):
        query = {
            "username": username,
            "password": password,
            "unit_id":  unit_id,
        }

        print(query)

        result = self.user_collection.find_one(query)

        if result is None:
            return None

        match result["role"]:
            case "admin":
                return Admin.from_dict(result)
            case "supervisor":
                return Supervisor.from_dict(result)
            case "employee":
                return Employee.from_dict(result)


    # change the password of the user with the corresponding id
    def change_password(self, id: str, password: str) -> bool:
        result = self.user_collection.find_one_and_update(
            {"id": id},
            {"$set": {"password": password}}
        )

        if result is None:
            return False

        return True
