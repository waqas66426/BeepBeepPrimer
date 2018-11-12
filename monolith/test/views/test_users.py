from unittest import TestCase


class test_users(TestCase):
    def setUp(self):
        from monolith.app import create_app
        self.app = create_app()
        self.app_test_cleint = self.app.test_client()

    def test_create_user_form_avaibility(self):
        response = self.app_test_cleint.get('/create_user', follow_redirects=True)
        self.assertEqual(response.status, '200 OK')

    def test_create_user(self):
        response = self.app_test_cleint.post('/create_user', data=dict(email="corradoPisa1@gmail.com",
            firstname="corrado", lastname="Pisa", password="password", age=10, weight=10, 
            max_hr=10, rest_hr=10, vo2max=10), follow_redirects=True)
        self.assertEqual(response.status, '200 OK')

    def tets_delete_user(self):
        response = self.app_test_cleint.post('/delete_user', follow_redirects=True)
        self.assertEqual(response.status, '200 OK')