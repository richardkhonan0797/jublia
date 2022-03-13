from app import db
from app.tests.conftest import TestBase

from app.models.email_content_model import EmailContent


class TestManageEmail(TestBase):
    def setUp(self, app, client):
        db.create_all()

    def tearDown(self, app, client):
        db.session.remove()
        db.drop_all()

    def test_get_manage_email(self, app, client):
        email_content = [
            EmailContent(
                event_id=1,
                email_subject="😋 Лорем",
                email_content="Лорем ипсум долор сит амет, но пер утинам луптатум адолесценс, яуо цонгуе алияуандо ид. Усу не новум утамур доцен",
                timestamp="15 Dec 2015 13:13"
            ),
            EmailContent(
                event_id=2,
                email_subject="Subject",
                email_content="Content",
                timestamp="15 Dec 2015 13:13"
            )
        ]
        db.session.add_all(email_content)
        db.session.commit()

        response = client.get(
            f'/manage_email'
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.get_json()['data']))
        

    def test_delete_manage_email(self, app, client):
        email_content = EmailContent(
            event_id=1,
            email_subject="😋 Лорем",
            email_content="Лорем ипсум долор сит амет, но пер утинам луптатум адолесценс, яуо цонгуе алияуандо ид. Усу не новум утамур доцен",
            timestamp="15 Dec 2015 13:13"
        )
        db.session.add(email_content)
        db.session.commit()

        response = client.delete(
            f'/manage_email?email_content_id={email_content.id}',
        )

        self.assertEqual(200, response.status_code)

    def test_delete_manage_email_form_error(self, app, client):
        response = client.delete(
            '/manage_email',
        )

        self.assertEqual(422, response.status_code)
