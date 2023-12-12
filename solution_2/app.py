"""Flask notes app."""

import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

import routes_auth
import routes_home
import routes_notes
import routes_users
from models import connect_db, bcrypt


def create_app(**config):
    """Set up and return Flask app (pass kwargs to override default config)."""

    app = Flask(__name__, root_path=".")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", "postgresql:///flask_notes"),
        SQLALCHEMY_ECHO=True,
        SECRET_KEY="abc123",
    )
    app.config.update(config)

    DebugToolbarExtension(app)

    connect_db(app)
    bcrypt.init_app(app)

    app.register_blueprint(routes_auth.bp)
    app.register_blueprint(routes_home.bp)
    app.register_blueprint(routes_notes.bp)
    app.register_blueprint(routes_users.bp)

    return app
