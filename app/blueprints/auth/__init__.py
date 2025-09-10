from flask import Blueprint, jsonify, url_for, request, session, redirect, render_template
from app.model import employee
from app.model.admin import Admin
from app.model.supervisor import Supervisor
from app.blueprints.names import ADMIN_BP, EMPLOYEE_BP, AUTH_BP, SUPERVISOR_BP, USER_BP
from app.services.user_service import UserService


def create_auth_blueprint(user_service: UserService) -> Blueprint:
    auth_bp = Blueprint(AUTH_BP, __name__, template_folder="templates")


    @auth_bp.route("/login", methods=["GET", "POST"])
    def login():
        error = None


        """
        TODO UNCOMMENT THESE
        THEY ARE ONLY COMMENTED FOR TESTING
        """

        # if request.method != "POST":
        #     return render_template("auth/login.html")
        #
        # username = request.form["username"]
        # password = request.form["password"]
        # unit_id  = request.form["unit_id"]
        username = "js"
        password = "12"
        unit_id = "u1"

        user = user_service.get_user(username, password, unit_id)

        if user is None:
            error = "Invalid credentials"
            return render_template(f"{AUTH_BP}/login.html", error=error)

        session["user_id"] = user.id
        session["unit_id"] = user.unit_id
        session["role"]    = user.role

        return redirect(url_for(f"{USER_BP}.dashboard", role=session["role"]))


    @auth_bp.route("/logout", methods=["GET"])
    def logout():
        session.pop("employee_id")
        session.pop("supervisor_id")
        session.pop("admin_id")
        return redirect(url_for(f"{AUTH_BP}.login"))


    @auth_bp.route("/permissions", methods=["GET"])
    def missing_permissions():
        return render_template(f"{AUTH_BP}/missing_permissions.html")

    return auth_bp

