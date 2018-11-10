from unittest import TestCase
from flask_login import user_logged_in


class test_auth(TestCase):
    def setUp(self):
        from monolith.app import create_app
        app = create_app()
        self.app = app.test_client()
        self.current_user = user_logged_in

    def test_logout(self):
        response = self.app.open('logout', follow_redirects=True)
        self.assertEqual(response.status, '200 OK')
