from typing import List, Optional
from flask import Blueprint, request, render_template, session
from app.blueprints.names import PRODUCT_BP
from app.exceptions.exceptions import ProductNotFoundByIdError, UnitNotFoundByIdError
from app.model.product import Product
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.utils.auth_utils import is_admin_logged_in, login_required, required_role


def create_product_blueprint(prod_repo: ProductRepository, product_service: ProductService):
    product_bp = Blueprint(PRODUCT_BP, __name__, template_folder="templates")


    @product_bp.route("/products", methods=["GET"])
    @login_required
    @required_role("employee")
    def get_all_products():
        products: Optional[List]
        view_products_page = "product/view_products.html"

        if is_admin_logged_in():
            try:
                products = product_service.get_products()
            except ValueError:
                return render_template(view_products_page, error="No products found")
        else:
            try:
                products = product_service.get_products_from_unit(session["unit_id"])
            except UnitNotFoundByIdError:
                return render_template(view_products_page, error="Could not find your unit.")
            except ValueError:
                return render_template(
                    view_products_page,
                    error="The product's record in the database is missing required attributes.",
                )

        return render_template(view_products_page, products=[product.to_dict() for product in products])


    @product_bp.route("/search-products", methods=["GET", "POST"])
    @login_required
    @required_role("employee")
    def search_products():
        error: str                          = ""
        products: List[Product]             = []
        start_index_int: Optional[int]      = None
        end_index_int: Optional[int]        = None
        search_products_page: str           = "product/search_products.html"

        if request.method != "POST":
            return render_template(search_products_page)

        # if the field is falsy (here it can be empty string "") assign None
        # 0 can be falsy, but this is not a problem because if 0 is entered in form
        # min_quantity will be "0" which is not falsy
        order_field: Optional[str]   = request.form.get("order_field") or None
        order_type: Optional[str]    = request.form.get("order_type") or None
        product_name: Optional[str]  = request.form.get("product_name") or None
        product_id: Optional[str]    = request.form.get("product_id") or None
        min_quantity: Optional[str]  = request.form.get("start_index") or None
        max_quantity: Optional[str]  = request.form.get("end_index") or None
        unit_id: Optional[str]       = session.get("unit_id")

        # are both present?
        if min_quantity not in ("", None) and max_quantity not in ("", None):
            try:
                start_index_int = int(min_quantity)
                end_index_int   = int(max_quantity)
            except ValueError:
                error = "From and To fields must be numbers"
                return render_template(search_products_page, error=error, products=products)

        try:
            products = product_service.search_products(order_field, order_type, product_name, product_id, start_index_int, end_index_int, unit_id)
        except ValueError:
            error = "Invalid prices for range fields."
            return render_template(search_products_page, error=error)

        if not products:
            error = "No products found"
            return render_template(search_products_page, error=error)

        return render_template(search_products_page, error=error, products=products)


    @product_bp.route("/view-product", methods=["GET", "POST"])
    @product_bp.route("/products/<product_id>", methods=["GET"])
    @login_required
    @required_role("employee")
    def view_product(product_id: Optional[str] = None):
        error: str = ""
        product: Optional[Product] = None
        view_product_page: str = "product/view_product.html"

        # Case 1: Came here after viewing all products and choosing one
        if product_id:
            product = prod_repo.get_product_by_id(product_id)
            try:
                product = product_service.get_product_by_id(product_id)
            except ProductNotFoundByIdError:
                return render_template(
                    view_product_page,
                    error="Could not find product.",
                )
            except ValueError:
                return render_template(
                    view_product_page,
                    error="The product's record in the database is missing required attributes.",
                )

            return render_template(
                view_product_page, product=product, product_id=product_id
            )

        # Case 2: manual search by entering a product's id
        # The user enters the products id
        # If GET just show the page
        if request.method != "POST":
            return render_template(
                view_product_page,
                error      = error,
                product    = product,
                product_id = product_id
            )

        product_id = request.form.get("product_id")

        if not product_id:
            error = "Please enter a products id"
            return render_template(
                view_product_page,
                error      = error, 
                product    = product,
                product_id = product_id
            )

        product = prod_repo.get_product_by_id(product_id)

        if product is None:
            error = "No products found"

        return render_template(
            view_product_page,
            error      = error, 
            product    = product,
            product_id = product_id
        )


    @login_required
    @required_role("employee")
    def sell_product():
        pass


    return product_bp
