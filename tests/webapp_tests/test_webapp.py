from salvius import webapp
from unittest import TestCase


class WebAppTestCase(TestCase):

    def setUp(self):
        webapp.app.config['TESTING'] = True
        self.app = webapp.app.test_client()

    def test_get_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.data)

    def test_get_javascript_assets(self):
        response = self.app.get('/js/assets.min.js')
        self.assertEqual(response.status_code, 200)

    def test_get_stylesheet_assets(self):
        response = self.app.get('/css/assets.min.css')
        self.assertEqual(response.status_code, 200)
