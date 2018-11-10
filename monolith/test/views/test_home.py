from flask_testing import TestCase



class test_home(TestCase):

    def create_app(self):
        from monolith.app import create_app
        return create_app()

    def test_index(self):
        self.client.get('/')
        self.assertTemplateUsed('index.html')

        from stravalib import Client
        client = Client()
        client_id = self.app.config['STRAVA_CLIENT_ID']
        redirect = 'http://127.0.0.1:5000/strava_auth'
        url = client.authorization_url(client_id=client_id, redirect_uri=redirect)
        self.assertContext("strava_auth_url", url)
        self.assertContext("runs", None)
