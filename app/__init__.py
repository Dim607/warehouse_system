import os
from pymongo import MongoClient
from app.blueprints.auth import create_auth_blueprint
from app.blueprints.employee import create_employee_blueprint
from app.blueprints.product import create_product_blueprint
from app.custom_flask import CustomFlask
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository


def create_server():
    # server = Flask(__name__)
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
    client                = MongoClient(server.config["MONGO_HOST"], server.config["MONGO_PORT"])
    db                    = client[server.config["MONGO_DATABASE"]]
    admin_collection      = db["admin"]
    unit_collection       = db["unit"]
    product_collection    = db["product"]
    user_collection       = db["user"]

    # Attach to server
    server.db                    = db
    server.admin_collection      = admin_collection
    server.unit_collection       = unit_collection
    server.product_collection    = product_collection
    server.user_collection       = user_collection

    # Initialize repositories
    emp_repo = EmployeeRepository(server.user_collection)
    # sup_repo = 
    # adm_repo = 
    # unt_repo = 
    prd_repo = ProductRepository(server.product_collection)
    usr_repo = UserRepository(server.user_collection)

    # Add blueprints for routes
    # server.register_blueprint(employee_routes.create_employee_blueprint(emp_repo, prd_repo))
    server.register_blueprint(create_auth_blueprint(emp_repo))
    server.register_blueprint(create_employee_blueprint(usr_repo, emp_repo, prd_repo))
    server.register_blueprint(create_product_blueprint(prd_repo))

    return server
