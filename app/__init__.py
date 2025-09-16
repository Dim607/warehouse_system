import os
from pymongo import MongoClient
from app.blueprints.auth import create_auth_blueprint
from app.blueprints.employee import create_employee_blueprint
from app.blueprints.product import create_product_blueprint
from app.blueprints.supervisor import create_supervisor_blueprint
from app.blueprints.user import create_user_blueprint
from app.custom_flask import CustomFlask
from app.model.unit import Unit
from app.repositories import product_repository
from app.repositories import unit_repository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.supervisor_repository import SupervisorRepository
from app.repositories.unit_repository import UnitRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService
from app.services.product_service import ProductService
from app.services.supervisor_service import SupervisorService
from app.services.user_service import UserService


def create_server():
    server = CustomFlask(__name__)

    server.config["SERVER_HOST"]       = os.environ.get("SERVER_HOST", "localhost")
    server.config["SERVER_PORT"]       = int(os.environ.get("SERVER_PORT", 5000))
    server.config["SERVER_SECRET_KEY"] = os.environ.get("SERVER_SECRET_KEY", os.urandom(24).hex())
    server.config["MONGO_DATABASE"]    = os.environ.get("MONGO_DATABASE", "LogisticsDB")
    server.config["MONGO_HOST"]        = os.environ.get("MONGO_HOST", "localhost")
    server.config["MONGO_PORT"]        = int(os.environ.get("MONGO_PORT", 27017))

    # to allow sessions
    server.secret_key = server.config["SERVER_SECRET_KEY"]

    # Initialize Mongodb clients
    client             = MongoClient(server.config["MONGO_HOST"], server.config["MONGO_PORT"])
    db                 = client[server.config["MONGO_DATABASE"]]
    admin_collection   = db["admin"]
    unit_collection    = db["units"]
    product_collection = db["products"]
    user_collection    = db["users"]

    # Create indexes to avoid duplicates
    unit_collection.create_index("id", unique=True)
    product_collection.create_index("id", unique=True)
    user_collection.create_index("id", unique=True)
    user_collection.create_index({"username": 1, "unit_id": 1}, unique=True)
    """ TODO add indexes for product collection """

    # Attach to server
    server.db                 = db
    server.admin_collection   = admin_collection
    server.unit_collection    = unit_collection
    server.product_collection = product_collection
    server.user_collection    = user_collection

    # Initialize repositories
    emp_repo = EmployeeRepository(server.user_collection)
    sup_repo = SupervisorRepository(server.user_collection)
    # adm_repo = 
    unt_repo = UnitRepository(unit_collection)
    prd_repo = ProductRepository(server.product_collection)
    usr_repo = UserRepository(server.user_collection)

    # Initialize services
    employee_service = EmployeeService(usr_repo, emp_repo, unt_repo)
    supervisor_service = SupervisorService(usr_repo, emp_repo, sup_repo, unt_repo)
    user_service     = UserService(usr_repo, unt_repo)
    product_service  = ProductService(prd_repo, unt_repo)

    # Add blueprints for routes
    server.register_blueprint(create_auth_blueprint(user_service))
    server.register_blueprint(create_employee_blueprint(employee_service, user_service))
    server.register_blueprint(create_user_blueprint(user_service))
    server.register_blueprint(create_product_blueprint(product_service))
    server.register_blueprint(create_supervisor_blueprint(supervisor_service, employee_service, user_service))

    return server
