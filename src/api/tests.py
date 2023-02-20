from django.test import TestCase

# Create your tests here.

class APITests(TestCase):
    def test_example(self):
        response = self.client.get('/api/example')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Hello World!')
