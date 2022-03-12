from app import db
from app.tests.conftest import TestBase


class TestSaveRecipient(TestBase):
    def setUp(self, app, client):
        db.create_all()

    def tearDown(self, app, client):
        db.session.remove()
        db.drop_all()


    def test_post_save_recipient(self, app, client):
        response = client.post(
            '/save_recipient',
            json={
                "event_id": 1,
                "email_recipient": "dummy@email.com",
            }
        )

        self.assertEqual(200, response.status_code)

    def test_post_save_recipient_form_error(self, app, client):
        response = client.post(
            '/save_recipient',
            json={}
        )

        self.assertEqual(422, response.status_code)
