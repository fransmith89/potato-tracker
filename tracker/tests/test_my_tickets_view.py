from django.test import Client, TestCase


class TestMyTicketsView(TestCase):
    def setup(self):
        self.client = Client()

    def test_landing_page_loads(self):
        res = self.client.get('/')

        self.assertEqual(res.status_code, 200)
