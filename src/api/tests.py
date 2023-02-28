from django.test import TestCase

# Create your tests here.


class APITests(TestCase):
    def test_example(self):
        response = self.client.get('/api/example')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Hello World!')

    def test_case(self):
        notes = "hejsan testet"
        medium = "email"
        customer_time = 123
        form_fill_time = 50
        response = self.client.post(
            "/api/case", {"notes": notes, "medium": medium, "customer_time": customer_time, "form_fill_time": form_fill_time, "category_id": 1}, content_type="application/json")

        self.assertEqual(response.status_code, 201)
