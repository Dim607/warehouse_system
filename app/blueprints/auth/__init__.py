from flask import Blueprint, url_for, request, session, redirect, render_template
from app.repositories.employee_repository import EmployeeRepository
from app.blueprints.names import EMPLOYEE_BP, AUTH_BP #type: ignore


def create_auth_blueprint(emp_repo: EmployeeRepository,) -> Blueprint:
    auth_bp = Blueprint(AUTH_BP, __name__, template_folder="templates")


    @auth_bp.route("/login", methods=["GET", "POST"])
    def login():
        error = None

        if request.method != "POST":
            return render_template("auth/login.html")

        username = request.form["username"]
        password = request.form["password"]
        unit_id  = request.form["unit_id"]
        employee = emp_repo.get_employee(username, password, unit_id)

        if employee is None:
            error = "Invalid credentials"
            return render_template("employee/employee_login.html", error=error)

        session["employee_id"] = employee.id
        return redirect(url_for(f"{EMPLOYEE_BP}.dashboard"))


    @auth_bp.route("/logout", methods=["GET"])
    def logout():
        session.pop("employee_id")
        return redirect(url_for(f"{AUTH_BP}.login"))


    return auth_bp

