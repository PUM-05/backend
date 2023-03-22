from datetime import timedelta
import json
from django.test import TestCase
from api.models import Category, Case

CASE_PATH = "/api/case"
JSON_PATH = "application/json"


class APITests(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name="test1")
        Category.objects.create(name="test2")
        Category.objects.create(name="test3")
        Category.objects.create(name="test4")
        p = Category.objects.create(name="test5")
        p2 = Category.objects.create(name="test51", parent=p)
        Category.objects.create(name="test52", parent=p)
        Category.objects.create(name="test511", parent=p2)

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
            additional_time = i + 1
            category = (i % 5) + 1

            dictionary = {"notes": notes, "medium": medium, "customer_time": customer_time,
                          "form_fill_time": form_fill_time, "additional_time": additional_time,
                          "category_id": category}

            response = self.client.post(CASE_PATH, dictionary, content_type=JSON_PATH)

            self.assertEqual(response.status_code, 201)

    def test_create_case_incorrect_category(self) -> None:
        category = 945
        notes = "notes"
        medium = "email"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post(CASE_PATH, dictionary, content_type=JSON_PATH)

        self.assertEqual(response.status_code, 400)

    def test_create_case_incorrect_medium(self) -> None:
        category = 5
        notes = "notes"
        medium = "tiktok"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post(CASE_PATH, dictionary, content_type=JSON_PATH)

        self.assertEqual(response.status_code, 400)

    def test_get_case_without_parameters(self) -> None:
        response = self.client.get(CASE_PATH)
        content = response.content.decode()
        data = json.loads(content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["medium"], None)
        self.assertEqual(data[1]["medium"], "phone")
        self.assertEqual(data[2]["medium"], "email")

    def test_nested_categories(self) -> None:
        response = self.client.get("/api/case/categories")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        data = json.loads(content)

        self.assertEqual(len(data), 8)
        self.assertEqual(data[3]["parent_id"], None)
        self.assertEqual(data[5]["parent_id"], 5)
        self.assertEqual(data[5]["parent_id"], 5)
        self.assertEqual(data[6]["parent_id"], 5)
        self.assertEqual(data[5]["parent_id"], 5)
