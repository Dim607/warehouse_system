from typing import Tuple
from flask import Blueprint, Request, Response, jsonify, url_for, request, session, redirect, render_template
# from flask import current_app
from app.repositories.employee_repository import EmployeeRepository


def create_employee_blueprint(emp_repo: EmployeeRepository) -> Blueprint:
    employee_bp = Blueprint("employee", __name__, url_prefix="/employee")
# emp_repo = EmployeeRepository.instance()

    @employee_bp.route("/", methods=["GET"])
    def home():
        if "employee_id" in session:
            return render_template("employee/employee_dashboard.html")
        return redirect(url_for("employee.login"))


    """
    employee_login()
    - Maybe enrypt the id before saving it in session variable
    """
    @employee_bp.route("/login", methods=["GET", "POST"])
    def login():
        error = None

        if request.method != "POST":
            return render_template("employee/employee_login.html")

        username = request.form['username']
        password = request.form['password']
        employee = emp_repo.get_employee(username, password)

        if employee is None:
            error = "Invalid credentials"
            return render_template("employee/employee_login.html", error=error)
        else:
            session["employee_id"] = employee.id

        return redirect(url_for("employee.dashboard"))

    @employee_bp.route("/logout", methods=["GET"])
    def logout():
        session.pop("employee_id")
        return redirect(url_for("employee.login"))

    @employee_bp.route("/dashboard", methods=["POST", "GET"])
    def dashboard():
        if "employee_id" not in session:
            return redirect(url_for("employee.login"))
        return render_template("employee/employee_dashboard.html")

    return employee_bp

# employee_bp = Blueprint("employee", __name__, url_prefix="/employee")
# # emp_repo = EmployeeRepository.instance()
#
# """
# employee_login()
# - Maybe enrypt the id before saving it in session variable
# """
#
# @employee_bp.route("/login", methods=["POST"])
# def login():
#     error = None
#
#     if request.method != "POST":
#         error = "Invalid request method"
#         return render_template("employee_login", error=error)
#
#     username = request.form['username']
#     password = request.form['password']
#
#     employee = emp_repo.get_employee(username, password)
#
#     if employee is None:
#         error = "Invalid credentials"
#         return render_template("employee_login", error=error)
#     else:
#         session["user_id"] = employee.id
#
#     return redirect(url_for("dashboard"))
#
# @employee_bp.route("/logout", methods=["GET"])
# def logout():
#     session.pop("user_id")
#     return redirect(url_for("login"))
#
# @employee_bp.route("/dashboard", methods=["POST", "GET"])
# def dashboard():
#     if session["employee_id"] is None:
#         return redirect(url_for("login"))
#     return render_template("dashboard.html")
