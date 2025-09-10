from typing import Optional
from flask import Blueprint, redirect, request, session, render_template, flash
from app.blueprints.names import EMPLOYEE_BP, USER_BP
from app.exceptions.exceptions import UnitNotFoundByIdError, UserNotFoundByIdError
from app.services.employee_service import EmployeeService
from app.services.user_service import UserService
from app.utils.auth_utils import login_required
from app.services.user_service import UserService


def create_user_blueprint(user_service: UserService):
    user_bp = Blueprint(USER_BP, __name__, template_folder="templates")

    return user_bp
