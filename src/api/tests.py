from datetime import timedelta
import json
from django.test import TestCase
from api.models import Category, Case


class APITests(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name="test1")
        Category.objects.create(name="test2")
        Category.objects.create(name="test3")
        Category.objects.create(name="test4")
        Category.objects.create(name="test5")

        Case.objects.create()
        Case.objects.create(medium="phone", form_fill_time=timedelta(seconds=5.3))
        Case.objects.create(medium="email", form_fill_time=timedelta(seconds=10),
                            additional_time=timedelta(seconds=20), notes="This is a note.",
                            customer_time=timedelta(seconds=90), category_id=3)

    def test_create_case_correct(self) -> None:
        for i in range(10):
            notes = "notes" + str(i)
            medium = "email" if i % 2 else "phone"
            customer_time = i
            form_fill_time = i
            additional_time = i+1
            category = (i % 5) + 1

            dictionary = {"notes": notes, "medium": medium, "customer_time": customer_time,
                          "form_fill_time": form_fill_time, "additional_time": additional_time,
                          "category_id": category}

            response = self.client.post("/api/case", dictionary, content_type="application/json")

            self.assertEqual(response.status_code, 201)

    def test_create_case_incorrect_category(self) -> None:
        category = 6
        notes = "notes"
        medium = "email"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post("/api/case", dictionary, content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_create_case_incorrect_medium(self) -> None:
        category = 5
        notes = "notes"
        medium = "tiktok"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post("/api/case", dictionary, content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_get_case_without_parameters(self) -> None:
        response = self.client.get("/api/case")
        content = response.content.decode()
        data = json.loads(content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["medium"], None)
        self.assertEqual(data[1]["medium"], "phone")
        self.assertEqual(data[2]["medium"], "email")
