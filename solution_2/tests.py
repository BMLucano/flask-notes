from unittest import TestCase

from app import create_app
from models import db, User, Note, bcrypt

app = create_app(
    BCRYPT_LOG_ROUNDS=4,
    DEBUG_TB_ENABLED=False,
    SQLALCHEMY_DATABASE_URI='postgresql:///flask_notes_test',
    SQLALCHEMY_ECHO=False,
    TESTING=True,
    WTF_CSRF_ENABLED=False,
)

print("Tests: dropping and recreating tables")
db.drop_all()
db.create_all()

PASSWORD_HASH = bcrypt.generate_password_hash("password").decode("utf-8")

USER_1 = {
    "username": "user-1",
    "password": PASSWORD_HASH,
    "email": "user-1@email.com",
    "first_name": "First-1",
    "last_name": "Last-1",
}

NOTE_1 = {
    "title": "Title-1",
    "content": "Content-1",
    "owner_username": "user-1",
}


class BaseTestCase(TestCase):
    """Tests for User model."""

    def setUp(self):
        """Make demo data."""

        Note.query.delete()
        User.query.delete()

        u = User(**USER_1)
        n = Note(**NOTE_1)
        db.session.add_all([u, n])
        db.session.commit()

        self.note_id = n.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
