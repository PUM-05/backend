from django.test import TestCase
from api.models import Category
from django.contrib.auth.models import User


class APITests(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name="test1")
        Category.objects.create(name="test2")
        Category.objects.create(name="test3")
        Category.objects.create(name="test4")
        Category.objects.create(name="test5")

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
