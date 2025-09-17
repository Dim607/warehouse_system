from typing import List, Optional, Tuple
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from pymongo.errors import DuplicateKeyError
from app.blueprints.names import SUPERVISOR_BP
from app.exceptions.exceptions import UnitNotFoundByIdError, UserNotFoundByIdError
from app.model.employee import Employee
from app.services import employee_service
from app.services.employee_service import EmployeeService
from app.services.supervisor_service import SupervisorService
from app.services.user_service import UserService
from app.utils.auth_utils import login_required, required_role


def create_supervisor_blueprint(
    supervisor_service: SupervisorService,
    employee_service: EmployeeService,
    user_service: UserService
) -> Blueprint:
    supervisor_bp = Blueprint(SUPERVISOR_BP, __name__, template_folder="templates")

    def _try_insert_employee(
        name: str,
        surname: str,
        username: str,
        password: str,
        unit_id: str
    ) -> Optional[str]:
        error: Optional[str] = None
        try:
            insert_result = employee_service.insert_employee(
                name, surname, username, password, unit_id
            )
        except UnitNotFoundByIdError:
            error="Could not find your unit."
        except DuplicateKeyError:
            error="A user with the same username already exists in the unit."
        except ValueError:
            error="The user's record in the database is missing required attributes."
        return error


    def _try_delete_employee(employee_id: str, unit_id: Optional[str]):
        error: Optional[str] = None
        try:
            employee_service.delete_employee_by_id(employee_id, unit_id)
        except UnitNotFoundByIdError:
            error="Could not find your unit."
        except UserNotFoundByIdError:
            error = "Could not find employee."

        return error


    @supervisor_bp.route("/employee/create", methods=["GET", "POST"])
    @login_required
    @required_role("supervisor")
    def create_employee():
        create_employee_page = "supervisor/create_employee.html"

        if request.method != "POST":
            return render_template(create_employee_page)

        # get the field value or ""
        name: str     = request.form.get("name", "").strip()
        surname: str  = request.form.get("surname", "").strip()
        username: str = request.form.get("username", "").strip()
        password: str = request.form.get("password", "").strip()
        unit_id: str  = session["unit_id"]

        # if any variable had incorrect value
        if not all((name, surname, username, password)):
            return render_template(
                create_employee_page,
                error="All fields are required.",
                name=name,
                surname=surname,
                username=username,
            )

        error = _try_insert_employee(name, surname, username, password, unit_id)

        if error is not None:
            return render_template(
                create_employee_page,
                error=error,
                name=name,
                surname=surname,
                username=username,
            )

        flash("Employee created successfully.", "success")

        return redirect(url_for("supervisor.create_employee"))


    @supervisor_bp.route("/employees", methods=["GET", "POST"])
    @login_required
    @required_role("supervisor")
    def view_employees():
        # view all employees in unit, can select and delete employee
        view_employees_page       = "supervisor/view_employees.html"
        employees: List[Employee] = []
        unit_id: Optional[str]    = session.get("unit_id")
        error: Optional[str]      = None

        if unit_id is not None:
            employees = employee_service.get_employees_in_unit(unit_id)

        if request.method != "POST":
            return render_template(view_employees_page, employees=employees)

        employee_id = request.form.get("employee_id", "").strip()

        if not employee_id:
            return render_template(
                view_employees_page,
                error="This employee does not exist.",
                employees=employees,
            )

        error = _try_delete_employee(employee_id, unit_id)

        if error is not None:
            return render_template(
                view_employees_page, error=error, employees=employees
            )

        return redirect(url_for("supervisor.view_employees"))



    return supervisor_bp
