from flask import render_template, redirect, session, Blueprint
from werkzeug.exceptions import Unauthorized

from config import AUTH_KEY
from forms import RegisterForm, LoginForm, CsrfForm
from models import db, User

bp = Blueprint("auth", __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if AUTH_KEY in session:
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session[AUTH_KEY] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if AUTH_KEY in session:
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session[AUTH_KEY] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@bp.post("/logout")
def logout():
    """Logout route."""

    form = CsrfForm()

    if form.validate_on_submit():
        session.pop(AUTH_KEY)
        return redirect("/login")

    else:
        # didn't pass CSRF; ignore logout attempt
        raise Unauthorized()
