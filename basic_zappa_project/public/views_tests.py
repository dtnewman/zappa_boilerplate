from basic_zappa_project.test_utils import BaseTestCase


class TestViews(BaseTestCase):

    def test_status(self):
        expected = {'status': 'ok'}
        response = self.client.get('/status')
        self.assert200(response)
        self.assertEqual(response.json, expected)

    def test_about(self):
        response = self.client.get('/about')
        self.assert200(response)

    def test_home_get(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_register_get(self):
        response = self.client.get('/register')
        self.assert200(response)

