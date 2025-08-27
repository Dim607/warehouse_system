from typing import List, Optional
from flask import Blueprint, jsonify, url_for, request, session, redirect, render_template, flash
from app.blueprints.names import EMPLOYEE_BP
from app.model.product import Product
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.utils.auth_utils import login_required


def create_employee_blueprint(user_repo: UserRepository, emp_repo: EmployeeRepository, prod_repo: ProductRepository) -> Blueprint:
    employee_bp = Blueprint(EMPLOYEE_BP, __name__, url_prefix="/employee", template_folder="templates")


    @employee_bp.route("/", methods=["GET"])
    @login_required
    def dashboard():
        return render_template("employee/employee_dashboard.html")


    @employee_bp.route("/profile", methods=["GET"])
    @login_required
    def show_profile():
        employee = emp_repo.get_employee_by_id(session["employee_id"])

        if employee is None:
            error = "Could not find employee"
            return render_template("employee/profile.html", error=error)

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
    def change_password():
        error = None
        employee_id = session["employee_id"]

        if request.method != "POST":
            return render_template("employee/change-password.html")

        # the old password is used for verification
        password_old = request.form.get("password_old")
        password_new = request.form.get("password_new")

        if password_old == "" or password_new == "" or password_old is None or password_new is None:
            error = "Both fields are required"
            return render_template("employee/change-password.html", error=error)

        if password_old == password_new:
            error = "Previous password cannot be the same as new password"
            return render_template("employee/change-password.html", error=error)

        employee = emp_repo.get_employee_by_id(employee_id)

        if employee is None:
            error = "Could not find employee"
            return render_template("employee/change-password.html", error=error)

        if employee.password != password_old:
            error = "Previous password is incorrect"
            return render_template("employee/change-password.html", error=error)

        is_password_changed = user_repo.change_password(employee_id, password_new) 

        if is_password_changed is False:
            error = "Could not change password"
            return render_template("employee/change-password.html", error=error)

        flash("Password successfully changed!", "success")
        return render_template("employee/change-password.html")


    return employee_bp
