from flask import render_template, redirect, session, Blueprint
from werkzeug.exceptions import Unauthorized

from forms import CsrfForm
from models import db, User, Note

from config import AUTH_KEY

bp = Blueprint("users", __name__)


@bp.get("/users/<username>")
def show_user(username):
    """Show user & notes page for logged-in-users."""

    if AUTH_KEY not in session or username != session[AUTH_KEY]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    form = CsrfForm()

    return render_template("users/show.html", user=user, form=form)


@bp.post("/users/<username>/delete")
def remove_user(username):
    """Remove user and redirect to login."""

    if AUTH_KEY not in session or username != session[AUTH_KEY]:
        raise Unauthorized()

    form = CsrfForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        Note.query.filter_by(owner_username=username).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop(AUTH_KEY)

        return redirect("/login")

    else:
        # didn't pass CSRF
        raise Unauthorized()
