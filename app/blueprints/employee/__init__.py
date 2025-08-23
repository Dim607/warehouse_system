from typing import List, Optional
from flask import Blueprint, jsonify, url_for, request, session, redirect, render_template
from app.blueprints.names import EMPLOYEE_BP, AUTH_BP #type: ignore
from app.model.product import Product
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository


def create_employee_blueprint(emp_repo: EmployeeRepository, prod_repo: ProductRepository) -> Blueprint:
    employee_bp = Blueprint(EMPLOYEE_BP, __name__, url_prefix="/employee")

    @employee_bp.route("/", methods=["GET"])
    def home():
        if "employee_id" in session:
            return render_template("employee/employee_dashboard.html")
        return redirect(url_for(f"{AUTH_BP}.login"))


    @employee_bp.route("/dashboard", methods=["POST", "GET"])
    def dashboard():
        if "employee_id" not in session:
            return redirect(url_for(f"{AUTH_BP}.login"))
        return render_template("employee/employee_dashboard.html")


    @employee_bp.route("/profile", methods=["GET"])
    def show_profile():
        if "employee_id" not in session:
            return redirect(url_for(f"{AUTH_BP}.login"))

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
            return redirect(url_for(f"{AUTH_BP}.login"))

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


    @employee_bp.route("products", methods=["GET", "POST"])
    def get_all_products():
        error = None
        products: List | None

        if "employee_id" not in session:
            return redirect(url_for(f"{AUTH_BP}.login"))

        if request.method != "POST":
            return render_template("employee/view_products.html")

        products = prod_repo.get_products()

        if not products:
            error = "No products found"

        return render_template("employee/products.html", error=error, products=[product.to_dict() for product in products])


    @employee_bp.route("search-products", methods=["GET", "POST"])
    def search_products():
        error: str = ""
        products: List[Product] = []
        start_index_int: int
        end_index_int: int

        if "employee_id" not in session:
            return redirect(url_for(f"{AUTH_BP}.login"))

        if request.method != "POST":
            return render_template("employee/search_products.html")

        order_field: Optional[str]  = request.form.get("order_field")
        order_type: Optional[str]   = request.form.get("order_type")
        product_name: Optional[str] = request.form.get("product_name")
        product_id: Optional[str]   = request.form.get("product_id")
        start_index: Optional[str]  = request.form.get("start_index")
        end_index: Optional[str]    = request.form.get("end_index")

        if start_index is not None and end_index is not None:
            try:
                start_index_int = int(start_index)
                end_index_int   = int(end_index)
            except:
                error = "From and To fields must be numbers"
                return render_template("search_products.html", error=error, products=products)

        # is order_field valid?
        if order_field != "name" and order_field != "quantity":
            products = prod_repo.search_products(None, None, product_name, product_id, start_index_int, end_index_int)
        else:
        # No need to check order_type, ascending is default unless descending is specified
            products = prod_repo.search_products(order_field, order_type, product_name, product_id, start_index_int, end_index_int)

        if not products:
            error = "No products found"
            return render_template("search_products.html", error=error, products=products)

        return render_template("search_products.html", error=error, products=products)


    @employee_bp.route("/view-product", methods=["GET", "POST"])
    @employee_bp.route("/products/<product_id>", methods=["GET"])
    def view_product(product_id: Optional[str] = None):
        error: str = ""
        product: Optional[Product] = None

        if "employee_id" not in session:
            return redirect(url_for(f"{AUTH_BP}.login"))

        # Case 1: clicked on info link
        if product_id:
            product = prod_repo.get_product_by_id(product_id)
            if product is None:
                error = "No products found"
            return render_template(
                "employee/view_product",
                error      = error, 
                product    = product,
                product_id = product_id
            )

        # Case 2: manual search
        # The user enters the products id
        # If GET just show the page
        if request.method != "POST":
            return render_template(
                "employee/view_product",
                error      = error, 
                product    = product,
                product_id = product_id
            )

        product_id = request.form.get("product_id")

        if not product_id:
            error = "Please enter a products id"
            return render_template(
                "employee/view_product",
                error      = error, 
                product    = product,
                product_id = product_id
            )

        product = prod_repo.get_product_by_id(product_id)

        if product is None:
            error = "No products found"

        return render_template(
            "employee/view_product",
            error      = error, 
            product    = product,
            product_id = product_id
        )


    def sell_product():
        return jsonify({}), 200


    return employee_bp
