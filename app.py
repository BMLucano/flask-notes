import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, NoteForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

AUTH_KEY = 'username'

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """ Shows homepage """

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def register_form():
    """
    Shows form, when submitted will register/create a user
    Form accepts a username, password, email, first_name, and last_name
    """
    if "username" in session:
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        # can add user in register function but always commit in route
        db.session.add(user)
        db.session.commit()

        session[AUTH_KEY] = user.username

        return redirect(f"/users/{user.username}")

    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_form():
    """
    Shows a login form that when submitted will login a user
    This form accepts a username and a password
    """
    if "username" in session:
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session[AUTH_KEY] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(AUTH_KEY, None)
        return redirect("/")
    else:
        raise Unauthorized()


@app.post("/users/<username>/delete")
def delete_user(username):
    """Delete user and their notes."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        user = User.query.get(username)
        notes = Note.query.get(user.notes).all()
        db.session.delete(notes)
        db.session.delete(user)
        db.session.commit()

        session.pop(AUTH_KEY)

        return redirect("/")
    else:
        raise Unauthorized()


@app.get("/users/<username>")
def show_user(username):
    """Show info and notes about a logged in user"""

    if "username" not in session or username != session[AUTH_KEY]:
        flash("Unauthorized access!")
        return redirect("/login")

    user = User.query.get_or_404(username)
    user_notes = Note.query.filter_by(owner_username=username).all()
    print("###################user notes=", user_notes)
    form = CSRFProtectForm()

    return render_template("user_info.html", user=user, form=form, notes=user_notes)


@app.route("/users/<username>/notes/add", methods=['GET', 'POST'])
def add_note(username):
    """Display form to add notes. Add note to DB and redirect"""

    form = NoteForm()
    user = User.query.get(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title,
                        content=content,
                        username=username)
        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("create_note.html", form=form, user=user)

