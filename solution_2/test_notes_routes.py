from models import db, Note
from tests import BaseTestCase, app


class NoteRoutesTestCase(BaseTestCase):
    """Tests for User routes."""

    def test_new_note_unauth(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.get(
                "/users/user-1/notes/new",
            )
            self.assertEqual(resp.status_code, 401)

    def test_new_note_404(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.get(
                "/users/wrong/notes/new",
            )
            self.assertEqual(resp.status_code, 404)

    def test_new_note_form(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.get(
                "/users/user-1/notes/new",
            )
            html = resp.get_data(as_text=True)
            self.assertIn("TEST: notes/new.html", html)

    def test_new_note_ok(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.post(
                "/users/user-1/notes/new",
                data={
                    "title": "Title",
                    "content": "Content",
                }
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/user-1")

            self.assertEqual(Note.query.count(), 2)

    def test_update_note_unauth(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.get(
                f"/notes/{self.note_id}/update",
            )
            self.assertEqual(resp.status_code, 401)

    def test_update_note_404(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.get(
                f"/notes/0/update",
            )
            self.assertEqual(resp.status_code, 404)

    def test_update_note_form(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.get(
                f"/notes/{self.note_id}/update",
            )
            html = resp.get_data(as_text=True)
            self.assertIn("TEST: notes/edit.html", html)

    def test_update_note_ok(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.post(
                f"/notes/{self.note_id}/update",
                data={
                    "title": "NewTitle",
                    "content": "NewContent",
                }
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/user-1")

            n = db.session.get(Note, self.note_id)
            self.assertEqual(n.title, "NewTitle")
            self.assertEqual(n.content, "NewContent")

    def test_delete_note(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.post(
                f"/notes/{self.note_id}/delete",
            )
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/user-1")
            self.assertIsNone(db.session.get(Note, self.note_id))

    def test_delete_note_unauth(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "wrong"
            resp = client.post(
                f"/notes/{self.note_id}/delete",
            )
            self.assertEqual(resp.status_code, 401)

    def test_delete_note_404(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "user-1"
            resp = client.post(
                f"/notes/0/delete",
            )
            self.assertEqual(resp.status_code, 404)
