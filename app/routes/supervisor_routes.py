from flask import Blueprint, Request, jsonify, url_for, current_app
from app.repositories.employee_repository import EmployeeRepository

supervisor_bp = Blueprint("supervisor", __name__, url_prefix="/supervisor")

