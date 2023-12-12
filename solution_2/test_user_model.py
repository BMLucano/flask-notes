from models import User, db, bcrypt
from tests import BaseTestCase


class UserModelTestCase(BaseTestCase):
    """Tests for User model."""

    def test_register(self):
        User.register("uname", "pwd", "First", "Last", "e@e.com")
        db.session.commit()

        u = db.session.get(User, "uname")
        self.assertTrue(bcrypt.check_password_hash(u.password, "pwd"))

    def test_auth_ok(self):
        u = db.session.get(User, "user-1")
        self.assertEqual(User.authenticate("user-1", "password"), u)

    def test_auth_fail_no_user(self):
        self.assertFalse(User.authenticate("user-X", "password"))

    def test_auth_ok_wrong_pwd(self):
        u = db.session.get(User, "user-1")
        self.assertFalse(User.authenticate("user-1", "wrong"))
