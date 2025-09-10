from typing import Optional
from flask import Blueprint, redirect, request, session, render_template, flash
from app.blueprints.names import EMPLOYEE_BP
from app.exceptions.exceptions import UnitNotFoundByIdError, UserNotFoundByIdError
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService
from app.services.user_service import UserService
from app.utils.auth_utils import login_required, required_role


def create_employee_blueprint(
    emp_service: EmployeeService,
    user_service: UserService
) -> Blueprint:
    employee_bp = Blueprint(EMPLOYEE_BP, __name__, template_folder="templates")

    @employee_bp.route("/profile", methods=["GET"])
    @login_required
    @required_role("employee")
    def show_profile():
        employee_id: str = session["user_id"]
        try:
            employee = emp_service.get_employee_by_id(employee_id)
        except (UserNotFoundByIdError, UnitNotFoundByIdError):
            return render_template("employee/profile.html", error="Could not find employee")
        except ValueError:
            return render_template(
                "employee/profile.html",
                error="The user's record in the database is missing required attributes.",
            )

        return render_template(
            "employee/profile.html",
            name      = employee.name,
            surname   = employee.surname,
            username  = employee.username,
            unit_id   = employee.unit_id,
            unit_name = employee.unit_name
        )


    @employee_bp.route("/change-password", methods=["GET", "POST"])
    @login_required
    @required_role("employee")
    def change_password():
        employee_id = session["user_id"]

        if request.method != "POST":
            return render_template("employee/change-password.html")

        # the old password is used for verification
        password_old = request.form.get("password_old")
        password_new = request.form.get("password_new")

        if not password_old or not password_new:
            return render_template(
                "employee/change-password.html", error="Both fields are required."
            )

        if password_old == password_new:
            return render_template(
                "employee/change-password.html",
                error="Previous password cannot be the same as new password.",
            )

        try:
            employee = emp_service.get_employee_by_id(employee_id)
        except (UserNotFoundByIdError, UnitNotFoundByIdError):
            return render_template(
                "employee/change-password.html", error="Could not find employee."
            )
        except ValueError:
            return render_template(
                "employee/change-password.html",
                error="The user's record in the database is missing required attributes.",
            )

        if employee.password != password_old:
            return render_template(
                "employee/change-password.html", error="Previous password is incorrect."
            )

        is_password_changed = user_service.change_password(employee_id, password_new)

        if is_password_changed is False:
            return render_template(
                "employee/change-password.html", error="Could not change password."
            )

        flash("Password successfully changed!", "success")
        # return redirect(render_template("employee/change-password.html"))
        return render_template("employee/change-password.html")

    return employee_bp
