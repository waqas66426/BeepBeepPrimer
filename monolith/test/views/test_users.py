from unittest import TestCase


class test_users(TestCase):
    def setUp(self):
        from monolith.app import create_app
        app = create_app()
        self.app = app.test_client()

    def test_create_user(self):
        response = self.app.post('/create_user', follow_redirects=True)
        self.assertEqual(response.status, '200 OK')
