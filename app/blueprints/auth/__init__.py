from flask import Blueprint, url_for, request, session, redirect, render_template
from app.model.admin import Admin
from app.model.supervisor import Supervisor
from app.blueprints.names import ADMIN_BP, EMPLOYEE_BP, AUTH_BP, SUPERVISOR_BP
from app.repositories.user_repository import UserRepository


def create_auth_blueprint(user_repo: UserRepository,) -> Blueprint:
    auth_bp = Blueprint(AUTH_BP, __name__, template_folder="templates")


    @auth_bp.route("/login", methods=["GET", "POST"])
    def login():
        error = None

        if request.method != "POST":
            return render_template("auth/login.html")

        username = request.form["username"]
        password = request.form["password"]
        unit_id  = request.form["unit_id"]

        user = user_repo.get_user(username, password, unit_id)

        # if user is None:
        #     error = "Invalid credentials"
        #     return render_template("employee/employee_login.html", error=error)
        #
        # session["employee_id"] = user.id
        # return redirect(url_for(f"{EMPLOYEE_BP}.dashboard"))


        if user is None:
            error = "Invalid credentials"
            return render_template("employee/employee_login.html", error=error)

        if isinstance(user, Admin):
            session["admin_id"] = user.id
            return redirect(url_for(f"{ADMIN_BP}.dashboard"))

        if isinstance(user, Supervisor):
            session["supervisor_id"] = user.id
            return redirect(url_for(f"{SUPERVISOR_BP}.dashboard"))

        session["employee_id"] = user.id
        return redirect(url_for(f"{EMPLOYEE_BP}.dashboard"))


    @auth_bp.route("/logout", methods=["GET"])
    def logout():
        session.pop("employee_id")
        session.pop("supervisor_id")
        session.pop("admin_id")
        return redirect(url_for(f"{AUTH_BP}.login"))


    return auth_bp

