from flask import Blueprint
from flask import render_template, redirect, session
from werkzeug.exceptions import Unauthorized

from config import AUTH_KEY
from forms import NoteAddForm, NoteEditForm, CsrfForm
from models import db, User, Note

bp = Blueprint("notes", __name__)


@bp.route("/users/<username>/notes/new", methods=["GET", "POST"])
def new_note(username):
    """Show add-note form and process it."""

    if AUTH_KEY not in session or username != session[AUTH_KEY]:
        raise Unauthorized()

    form = NoteAddForm()

    # make sure the user exists
    User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(
            title=title,
            content=content,
            owner_username=username,
        )

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        return render_template("notes/new.html", form=form)


@bp.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Show update-note form and process it."""

    note = Note.query.get_or_404(note_id)

    if AUTH_KEY not in session or note.owner_username != session[AUTH_KEY]:
        raise Unauthorized()

    form = NoteEditForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    return render_template("/notes/edit.html", form=form, note=note)


@bp.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Delete note."""

    note = Note.query.get_or_404(note_id)

    if AUTH_KEY not in session or note.owner_username != session[AUTH_KEY]:
        raise Unauthorized()

    form = CsrfForm()

    if form.validate_on_submit():  # <-- csrf checking!
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    else:
        # didn't pass CSRF
        raise Unauthorized()
