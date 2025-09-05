from  __future__ import annotations # for pyright typechecking
from typing import Any, Dict, List, Optional
import uuid


class Employee:
    id: Optional[str]
    name: str
    surname: str
    username: str
    password: str
    unit_id: str
    # unit_name is not saved in the database for each employee
    # because it can be found using unit_id
    # keep it here as a help field
    unit_name: Optional[str]
    role: str = "employee"

    def __init__(
        self,
        id: Optional[str],
        name: str,
        surname: str,
        username: str,
        password: str,
        unit_id: str,
        unit_name: Optional[str],
    ):
        self.id           = id if id is not None else str(uuid.uuid4())
        self.name         = name
        self.surname      = surname
        self.username     = username
        self.password     = password
        self.unit_id      = unit_id
        self.unit_name    = unit_name


    def __eq__(self, other: Employee) -> bool:
        return self.id == other.id


    def __str__(self) -> str:
        return ", ".join(map(str, [
            self.id,
            self.name,
            self.surname,
            self.username,
            self.password,
            self.unit_id,
            self.unit_name,
        ]))


    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"Employee({attrs})"


    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Employee object into a full dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing all attributes of the employee.
        """
        return {
            "id":        self.id,
            "name":      self.name,
            "surname":   self.surname,
            "username":  self.username,
            "password":  self.password,
            "unit_id":   self.unit_id,
            "unit_name": self.unit_name,
            "role":      self.role
        }


    def to_percistance_dict(self) -> dict[str, Any]:
        """
        Convert the Employee object into a dictionary suitable for persistence.

        This excludes fields that should not be stored in the database, such as 
        `unit_name`, which can be derived later by querying the unit collection.

        Returns:
            dict[str, Any]: A dictionary containing only the fields to persist in the database.
        """
        emp_dict = self.to_dict()
        emp_dict.pop("unit_name", None)
        return emp_dict


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Employee:
        """
        Returns an Employee instance from a dictionary


        Use this method to create an Employee object where `unit_name` is allowed to be missing.

        This method validates that all required attributes are present and non-None.
        Raises ValueError if any required attribute is missing.

        Args:
            data (dict): Dictionary containing the employee attributes.
            The following keys are required:
            - `name`
            - `surname`
            - `username`
            - `password`
            - `unit_id`
            - `unit_name`

        Returns:
            Employee: An Employee instance initialize with the given attributes

        Raises:
            ValueError: If any required attribute is missing or None.
        """

        # id can be None so dont include it in the attr list
        required_attrs = ["name", "surname", "username", "password", "unit_id", "unit_name"]
        return cls._from_dict(data, required_attrs)


    @classmethod
    def from_persistence_dict(cls, data: Dict[str, Any]) -> Employee:
        """
        Returns an Employee instance from a dictionary.

        Use this method to create an Employee object from a DB document 
        where `unit_name` is allowed to be missing.

        This method validates that all required attributes are present and non-None.
        Raises ValueError if any required attribute is missing.

        Args:
            data (dict): Dictionary containing the employee attributes.
            The following keys are required:
            - `name`
            - `surname`
            - `username`
            - `password`
            - `unit_id`

        Returns:
            Employee: An Employee instance initialized with the given attributes

        Raises:
            ValueError: If any required attribute is missing or None.
        """
        required_attrs = ["name", "surname", "username", "password", "unit_id"]
        return cls._from_dict(data, required_attrs)


    @classmethod
    def _from_dict(cls, data: dict[str, Any], required_attrs: List[str]) -> Employee:
        """
        Returns an Employee instance from a dictionary

        Validates that all required attributes are present and non-None.
        Raises ValueError if any required attribute is missing.

        Args:
            data (dict): Dictionary containing the employee attributes.
            require_attrs (List[str]): A list containing the names of all the required attributes.

        Returns:
            Employee: An Employee instance initialized with the given attributes

        Raises:
            ValueError: If any required attribute is missing or None.
        """
        for attr in required_attrs:
            if data.get(attr) is None:
                raise ValueError(f"Attribute {attr} cannot be None")

        employee = cls(
            id        = data.get("id"),
            name      = str(data["name"]),
            surname   = str(data["surname"]),
            username  = str(data["username"]),
            password  = str(data["password"]),
            unit_id   = str(data["unit_id"]),
            unit_name = data.get("unit_name"),
        )
        return employee


    def change_password(self, new_password: str) -> bool:
        if self.password == new_password:
            return False
        self.password = new_password
        return True
