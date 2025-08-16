import os
from pymongo import MongoClient
from app.custom_flask import CustomFlask
from app.routes import employee_routes, supervisor_routes, admin_routes


def create_server():
    # server = Flask(__name__)
    server = CustomFlask(__name__)

    server.config["SERVER_HOST"]       = os.environ.get("SERVER_HOST", "localhost")
    server.config["SERVER_PORT"]       = int(os.environ.get("SERVER_PORT", 5000))
    server.config["SERVER_SECRET_KEY"] = os.environ.get("SERVER_SECRET_KEY", "a_secret_key")
    server.config["MONGO_DATABASE"]    = os.environ.get("MONGO_DATABASE", "school_db")
    server.config["MONGO_HOST"]        = os.environ.get("MONGO_HOST", "localhost")
    server.config["MONGO_PORT"]        = int(os.environ.get("MONGO_PORT", 27017))

    # to allow sessions
    server.secret_key = server.config["SERVER_SECRET_KEY"]

    # Initialize Mongodb clients
    client                = MongoClient(server.config["MONGO_HOST"], server.config["MONGO_PORT"])
    db                    = client[server.config["MONGO_DATABASE"]]
    admin_collection      = db["admin"]
    unit_collection       = db["unit"]
    employee_collection   = db["employee"]
    supervisor_collection = db["supervisor"]
    product_collection    = db["product"]

    # Attach to server
    server.db                    = db
    server.admin_collection      = admin_collection
    server.unit_collection       = unit_collection
    server.employee_collection   = employee_collection
    server.supervisor_collection = supervisor_collection
    server.product_collection    = product_collection

    # Add blueprints for routes
    server.register_blueprint(employee_routes.employee_bp)
    server.register_blueprint(supervisor_routes.supervisor_bp)
    server.register_blueprint(admin_routes.admin_bp)

    return server
