from datetime import timedelta
import json
from django.test import TestCase
from api.models import Category, Case
from django.contrib.auth.models import User

CASE_PATH = "/api/case"
CONTENT_TYPE_JSON = "application/json"


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

        user1 = User.objects.create(username="user1")
        user1.set_password("")
        user1.save()
        user2 = User.objects.create(username="user2")
        user2.set_password("password2")
        user2.save()

    def test_login_correct(self) -> None:
        """
        Tests that the login endpoint returns a 200 status code and a session
        cookie when the login is successful.
        """
        response = self.client.post("/api/login", {"username": "user1"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.cookies["sessionid"].value) > 0)

        response = self.client.post("/api/login", {"username": "user2", "password": "password2"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.cookies["sessionid"].value) > 0)

    def test_login_incorrect(self) -> None:
        """
        Tests that the login endpoint returns a 401 status code when the login
        is unsuccessful.
        """
        response = self.client.post("/api/login", {"username": "user1", "password": "wrong"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/login", {"username": "user2"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/login", {"username": "wrong"})
        self.assertEqual(response.status_code, 401)

    def test_logout(self) -> None:
        """
        Tests that the logout endpoint returns a 200 status code when the user
        is logged in and a 401 status code when the user is not logged in.
        """
        response = self.client.get("/api/logout")
        self.assertEqual(response.status_code, 401)

        self.client.login(username="user1", password="")

        response = self.client.get("/api/logout")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/check")
        self.assertEqual(response.status_code, 401)

    def test_check(self) -> None:
        """
        Tests that the check endpoint returns a 200 status code when the user is
        logged in and a 401 status code when the user is not logged in.
        """
        response = self.client.get("/api/check")
        self.assertEqual(response.status_code, 401)

        self.client.login(username="user1", password="")

        response = self.client.get("/api/check")
        self.assertEqual(response.status_code, 200)

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

            response = self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

            self.assertEqual(response.status_code, 201)

    def test_create_case_incorrect_category(self) -> None:
        category = 945
        notes = "notes"
        medium = "email"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

        self.assertEqual(response.status_code, 400)

    def test_create_case_incorrect_medium(self) -> None:
        category = 5
        notes = "notes"
        medium = "tiktok"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

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
        self.assertEqual(data[6]["parent_id"], 5)
        self.assertEqual(data[5]["parent_id"], 5)
        self.assertEqual(data[7]["parent_id"], 6)

    def test_delete_case_correct_id(self) -> None:
        """
        Tests that the check endpoint returns a 200 status code when a case is found
        and deleted, as well as if the number of cases have changed and if querying a
        deleted object will result in an error.
        """
        no_cases_before = len(Case.objects.all())

        response = self.client.delete(CASE_PATH + "/1", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 204)

        no_cases_after = len(Case.objects.all())
        self.assertNotEqual(no_cases_before, no_cases_after)

        response = self.client.delete(CASE_PATH + "/2", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Case.DoesNotExist):
            Case.objects.get(id=2)

    def test_delete_case_incorrect_id(self) -> None:
        """
        Tests that the check endpoint returns a 404 status code when a case is queried
        with an incorrect id when trying to make a delete request, as well as if the
        number of cases remain the same.
        """
        no_cases_before = len(Case.objects.all())

        response = self.client.delete(CASE_PATH + "/128", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 404)
        response = self.client.delete(CASE_PATH + "/anders", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 404)
        response = self.client.delete(CASE_PATH + "/", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 404)

        no_cases_after = len(Case.objects.all())
        self.assertEqual(no_cases_before, no_cases_after)
