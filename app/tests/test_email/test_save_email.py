from app import db
from app.tests.conftest import TestBase


class TestSaveEmail(TestBase):
    def setUp(self, app, client):
        db.create_all()

    def tearDown(self, app, client):
        db.session.remove()
        db.drop_all()


    def test_post_save_email(self, app, client):
        response = client.post(
            '/save_emails',
            json={
                "event_id": 1,
                "email_subject": "Subject",
                "email_content": "Content",
                "timestamp": "15 Dec 2015 12:30"
            }
        )

        self.assertEqual(200, response.status_code)

    def test_post_save_email_form_error(self, app, client):
        response = client.post(
            '/save_emails',
            json={}
        )

        self.assertEqual(422, response.status_code)
