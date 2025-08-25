from functools import wraps
from flask import session, redirect, url_for
from app.blueprints.names import AUTH_BP


def login_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        if "employee_id" not in session:
            return redirect(
                url_for(f"{AUTH_BP}.login")
            )  # redirect to your one login route
        return f(**kwargs)

    return wrapped_view
