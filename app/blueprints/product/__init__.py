from typing import List, Optional
from flask import Blueprint, jsonify, url_for, request, session, redirect, render_template
from app.blueprints.names import PRODUCT_BP #type: ignore
from app.model.product import Product
from app.repositories.product_repository import ProductRepository
from app.utils.auth_utils import login_required


def create_product_blueprint(prod_repo: ProductRepository):
    product_bp = Blueprint(PRODUCT_BP, __name__, template_folder="templates")


    @product_bp.route("products", methods=["GET", "POST"])
    @login_required
    def get_all_products():
        error = None
        products: Optional[List]

        if request.method != "POST":
            return render_template("product/view_products.html")

        products = prod_repo.get_products()

        if not products:
            error = "No products found"

        return render_template("product/view_products.html", error=error, products=[product.to_dict() for product in products])


    @product_bp.route("search-products", methods=["GET", "POST"])
    @login_required
    def search_products():
        error: str = ""
        products: List[Product] = []
        start_index_int: int
        end_index_int: int

        if request.method != "POST":
            return render_template("product/search_products.html")

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
                return render_template("product/search_products.html", error=error, products=products)

        # is order_field valid?
        if order_field != "name" and order_field != "quantity":
            products = prod_repo.search_products(None, None, product_name, product_id, start_index_int, end_index_int)
        else:
        # No need to check order_type, ascending is default unless descending is specified
            products = prod_repo.search_products(order_field, order_type, product_name, product_id, start_index_int, end_index_int)

        if not products:
            error = "No products found"
            return render_template("product/search_products.html", error=error, products=products)

        return render_template("product/search_products.html", error=error, products=products)


    @product_bp.route("/view-product", methods=["GET", "POST"])
    @product_bp.route("/products/<product_id>", methods=["GET"])
    @login_required
    def view_product(product_id: Optional[str] = None):
        error: str = ""
        product: Optional[Product] = None

        # Case 1: clicked on info link
        if product_id:
            product = prod_repo.get_product_by_id(product_id)
            if product is None:
                error = "No products found"
            return render_template(
                "product/view_product",
                error      = error, 
                product    = product,
                product_id = product_id
            )

        # Case 2: manual search
        # The user enters the products id
        # If GET just show the page
        if request.method != "POST":
            return render_template(
                "product/view_product",
                error      = error, 
                product    = product,
                product_id = product_id
            )

        product_id = request.form.get("product_id")

        if not product_id:
            error = "Please enter a products id"
            return render_template(
                "product/view_product",
                error      = error, 
                product    = product,
                product_id = product_id
            )

        product = prod_repo.get_product_by_id(product_id)

        if product is None:
            error = "No products found"

        return render_template(
            "product/view_product",
            error      = error, 
            product    = product,
            product_id = product_id
        )


    @login_required
    def sell_product():
        return jsonify({}), 200
