from flask import session

from config import AUTH_KEY
from models import User, db, bcrypt
from tests import BaseTestCase, app


class UserRoutesTestCase(BaseTestCase):
    """Tests for User routes."""

    def test_homepage_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/register")

    def test_register_form(self):
        with app.test_client() as client:
            resp = client.get("/register")
            html = resp.get_data(as_text=True)
            self.assertIn("TEST: register.html", html)

    def test_register_ok(self):
        with app.test_client() as client:
            resp = client.post(
                "/register",
                data={
                    "username": "test",
                    "password": "password",
                    "first_name": "First",
                    "last_name": "Last",
                    "email": "e@e.com",
                }
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/test")

            u = db.session.get(User, "test")
            self.assertTrue(bcrypt.check_password_hash(u.password, "password"))

            self.assertEqual(session.get(AUTH_KEY), "test")

    def test_register_bad_form(self):
        with app.test_client() as client:
            resp = client.post(
                "/register",
                data={
                    "username": "much-much-much-much-much-much-much-too-long",
                    "password": "password",
                    "first_name": "First",
                    "last_name": "Last",
                    "email": "e@e.com",
                }
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Field cannot be longer than 20 characters.", html)

    def test_login_form(self):
        with app.test_client() as client:
            resp = client.get("/login")
            html = resp.get_data(as_text=True)
            self.assertIn("TEST: login.html", html)

    def test_login_ok(self):
        with app.test_client() as client:
            resp = client.post(
                "/login",
                data={
                    "username": "user-1",
                    "password": "password",
                }
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/user-1")
            self.assertEqual(session.get(AUTH_KEY), "user-1")

    def test_login_bad(self):
        with app.test_client() as client:
            resp = client.post(
                "/login",
                data={
                    "username": "user-1",
                    "password": "wrong-wrong",
                }
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid username/password", html)
            self.assertEqual(session.get(AUTH_KEY), None)

    def test_logout(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.post(
                "/logout",
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/login")
            self.assertEqual(session.get(AUTH_KEY), None)

    def test_show_user(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.get(
                "/users/user-1",
            )
            html = resp.get_data(as_text=True)
            self.assertIn("TEST: users/show.html", html)
            self.assertIn("First-1 Last-1", html)

    def test_show_user_unauth(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.get(
                "/users/user-1",
            )
            self.assertEqual(resp.status_code, 401)

    def test_show_user_404(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.get(
                "/users/wrong",
            )
            self.assertEqual(resp.status_code, 404)

    def test_remove_user(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.post(
                "/users/user-1/delete",
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/login")
            self.assertEqual(session.get(AUTH_KEY), None)

    def test_remove_user_unauth(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.post(
                "/users/user-1/delete",
            )
            self.assertEqual(resp.status_code, 401)

    def test_remove_user_404(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.post(
                "/users/wrong/delete",
            )
            self.assertEqual(resp.status_code, 404)
