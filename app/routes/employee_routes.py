from typing import List
from flask import Blueprint, jsonify, url_for, request, session, redirect, render_template
from app.model.product import Product
from app.repositories import product_repository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository


def create_employee_blueprint(emp_repo: EmployeeRepository, prod_repo: ProductRepository) -> Blueprint:
    employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

    @employee_bp.route("/", methods=["GET"])
    def home():
        if "employee_id" in session:
            return render_template("employee/employee_dashboard.html")
        return redirect(url_for("employee.login"))


    """
    employee_login()
    - Maybe enrypt the id before saving it in session variable
    """
    @employee_bp.route("/login", methods=["GET", "POST"])
    def login():
        error = None

        if request.method != "POST":
            return render_template("employee/employee_login.html")

        username = request.form["username"]
        password = request.form["password"]
        unit_id  = request.form["unit_id"]
        employee = emp_repo.get_employee(username, password, unit_id)

        if employee is None:
            error = "Invalid credentials"
            return render_template("employee/employee_login.html", error=error)

        session["employee_id"] = employee.id
        return redirect(url_for("employee.dashboard"))


    @employee_bp.route("/logout", methods=["GET"])
    def logout():
        session.pop("employee_id")
        return redirect(url_for("employee.login"))


    @employee_bp.route("/dashboard", methods=["POST", "GET"])
    def dashboard():
        if "employee_id" not in session:
            return redirect(url_for("employee.login"))
        return render_template("employee/employee_dashboard.html")


    @employee_bp.route("/profile", methods=["GET"])
    def show_profile():
        if "employee_id" not in session:
            return redirect(url_for("employee.login"))

        employee = emp_repo.get_employee_by_id(session["empoyee_id"])

        if employee is None:
            error = "Could not find employee"
            return render_template("employee/profile.html", error = error)

        return render_template(
            "employee/profile.html",
            name      = employee.name,
            surname   = employee.surname,
            username  = employee.username,
            unit_id   = employee.unit_id,
            unit_name = employee.unit_name
        )


    @employee_bp.route("/change-password", methods=["GET", "POST"])
    def change_password():
        error = None

        if "employee_id" not in session:
            return redirect(url_for("employee.login"))

        if request.method != "POST":
            return render_template("employee/change-password.html")

        employee_id = session["employee_id"]

        # the old password is used for verification
        password_old = request.form["password_old"]
        password_new = request.form["password_new"]

        employee = emp_repo.get_employee_by_id(employee_id)

        if employee is None:
            error = "Could not find employee"
            return render_template("employee/change-password.html", error=error)

        if employee.password != password_old:
            error = "Previous password is incorrect"
            return render_template("employee/change-password.html", error=error)

        is_password_changed = emp_repo.change_password(employee_id, password_new) 

        if is_password_changed is False:
            error = "Could not change password"
            return render_template("employee/change-password.html", error=error)

        return render_template("employee/change-password.html")


    @employee_bp.route("/view-products", methods=["GET", "POST"])
    def view_products():
        error = None
        products: List | None

        if "employee_id" not in session:
            return redirect(url_for("employee.login"))

        if request.method != "POST":
            return render_template("employee/view-products.html")

        products = prod_repo.get_products()

        if not products:
            error = "No products found"
            return render_template("employee/view-products.html", error=error)

        return render_template("employee/view-products.html", products=[product.to_dict() for product in products])


    @employee_bp.route("view-products", methods=["GET", "POST"])
    def search_products():
        error: str
        products: List[Product]

        if "employee_id" not in session:
            return redirect(url_for("employee.search_products"))

        if request.method != "POST":
            return render_template("employee/search_products.html")

        order_field: str  = request.form["order_field"]
        order_type: str   = request.form["order_type"]
        product_name: str = request.form["product_name"]
        product_id: str   = request.form["product_id"]
        start_index: str  = request.form["start_index"]
        end_index: str    = request.form["end_index"]

        # is order_field valid?
        if order_field != "name" and order_field != "quantity":
            products = prod_repo.search_products(None, None, product_name, product_id, int(start_index), int(end_index))
        # No need to check order_type, ascending is default unless descending is specified

        try:
            products = prod_repo.search_products(order_field, order_type, product_name, product_id, int(start_index), int(end_index))
        except:
            error = "Could not perform operation"
            return render_template("search_products.html", error=error)

        if not products:
            error = "No products found"
            return render_template("search_products.html", error=error)

        return render_template("search_products.html", products=products)


    def view_product():
        return jsonify({}), 200


    def sell_product():
        return jsonify({}), 200


    return employee_bp
