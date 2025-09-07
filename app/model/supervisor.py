from  __future__ import annotations # for pyright typechecking
from typing import Optional
from app.model.employee import Employee


class Supervisor(Employee):
    role: str = "supervisor"

    def __init__(
        self,
        id: Optional[str],
        name: str,
        surname: str,
        username: str,
        password: str,
        unit_id: str,
        unit_name: str,
    ):
        super().__init__(
            id,
            name,
            surname,
            username,
            password,
            unit_id,
            unit_name,
        )


    # it is not specified if the supervisor should also assign a username
    def create_employee(self, name: str, surname: str, username: str, password: str) -> Employee:
        employee = Employee(
            id        = None,
            name      = name,
            surname   = surname,
            username  = username,
            password  = password,
            unit_id   = self.unit_id,
            unit_name = self.unit_name,
        )
        return employee
