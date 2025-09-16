from typing import Optional
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from pymongo.errors import DuplicateKeyError
from app.blueprints.names import SUPERVISOR_BP
from app.exceptions.exceptions import UnitNotFoundByIdError
from app.services.employee_service import EmployeeService
from app.services.supervisor_service import SupervisorService
from app.services.user_service import UserService
from app.utils.auth_utils import login_required, required_role


def create_supervisor_blueprint(
    sup_service: SupervisorService,
    emp_service: EmployeeService,
    user_service: UserService
) -> Blueprint:
    supervisor_bp = Blueprint(SUPERVISOR_BP, __name__, template_folder="templates")

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

        try: 
            insert_result = emp_service.insert_employee(
                name, surname, username, password, unit_id
            )
        except UnitNotFoundByIdError:
            return render_template(
                create_employee_page,
                error="Could not find your unit.",
                name=name,
                surname=surname,
                username=username,
            )
        except DuplicateKeyError:
            return render_template(
                create_employee_page,
                error="A user with the same username already exists in the unit.",
            )
        except ValueError:
            return render_template(
                create_employee_page,
                error="The user's record in the database is missing required attributes.",
            )

        flash("Employee created successfully.", "success")

        return redirect(url_for("supervisor.create_employee"))


    return supervisor_bp
