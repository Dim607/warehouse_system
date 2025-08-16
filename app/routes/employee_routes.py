from flask import Blueprint, Request, jsonify, url_for, current_app
from app.repositories.employee_repository import EmployeeRepository

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

@employee_bp.route("/login", methods=["GET"])
def employee_start():
    return jsonify({"message": "Hello"}), 200
