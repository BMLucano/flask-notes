from flask import Blueprint
from flask import redirect

bp = Blueprint("home", __name__)


@bp.get("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/register")
