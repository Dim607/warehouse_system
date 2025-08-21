from flask import Blueprint, url_for, request, session, redirect, render_template
from app.repositories.employee_repository import EmployeeRepository


def create_employee_blueprint(emp_repo: EmployeeRepository) -> Blueprint:
    employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

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

        username = request.form["username"]
        password = request.form["password"]
        unit_id  = request.form["unit_id"]
        employee = emp_repo.get_employee(username, password, unit_id)

        if employee is None:
            error = "Invalid credentials"
            return render_template("employee/employee_login.html", error=error)

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


    @employee_bp.route("/profile", methods=["GET"])
    def show_profile():
        if "employee_id" not in session:
            return redirect(url_for("employee.login"))
        employee = emp_repo.get_employee_by_id(session["empoyee_id"])

        if employee is None:
            error = "Could not find employee"
            return render_template("employee/profile.html", error = error)

        return render_template(
            "employee/profile.html",
            name      = employee.name,
            surname   = employee.surname,
            username  = employee.username,
            unit_id   = employee.unit_id,
            unit_name = employee.unit_name
        )


    @employee_bp.route("/change-password", methods=["GET", "POST"])
    def change_password():
        error = None

        if "employee_id" not in session:
            return redirect(url_for("employee.login"))

        if request.method != "POST":
            return render_template("employee/change-password.html")

        employee_id = session["employee_id"]

        # the old password is used for verification
        password_old = request.form["password_old"]
        password_new = request.form["password_new"]

        employee = emp_repo.get_employee_by_id(employee_id)

        if employee is None:
            error = "Could not find employee"
            return render_template("employee/change-password.html", error=error)

        if employee.password != password_old:
            error = "Previous password is incorrect"
            return render_template("employee/change-password.html", error=error)

        is_password_changed = emp_repo.change_password(employee_id, password_new) 

        if is_password_changed is False:
            error = "Could not change password"
            return render_template("employee/change-password.html", error=error)

        return render_template("employee/change-password.html")


    return employee_bp
