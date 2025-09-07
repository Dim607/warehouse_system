from flask import Blueprint, jsonify, url_for, request, session, redirect, render_template
from app.model import employee
from app.model.admin import Admin
from app.model.supervisor import Supervisor
from app.blueprints.names import ADMIN_BP, EMPLOYEE_BP, AUTH_BP, SUPERVISOR_BP
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

        if isinstance(user, Admin):
            session["admin_id"] = user.id
            return redirect(url_for(f"{ADMIN_BP}.dashboard"))

        if isinstance(user, Supervisor):
            session["supervisor_id"] = user.id
            session["unit_id"] = unit_id
            return redirect(url_for(f"{SUPERVISOR_BP}.dashboard"))

        if isinstance(user, employee.Employee):
            session["employee_id"] = user.id
            session["unit_id"] = unit_id
            return redirect(url_for(f"{EMPLOYEE_BP}.dashboard"))

        """ TODO DO SOMETHING HERE"""
        return jsonify({"message": "Problem"}, 400)



    @auth_bp.route("/logout", methods=["GET"])
    def logout():
        session.pop("employee_id")
        session.pop("supervisor_id")
        session.pop("admin_id")
        return redirect(url_for(f"{AUTH_BP}.login"))


    return auth_bp

