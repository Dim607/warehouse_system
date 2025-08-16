from flask import Blueprint, Request, jsonify, url_for, current_app
from app.repositories.employee_repository import EmployeeRepository

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
