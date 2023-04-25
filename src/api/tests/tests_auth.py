from datetime import timedelta
from django.test import TestCase
from api.models import Category, Case
from django.contrib.auth.models import User

CONTENT_TYPE_JSON = "application/json"
LOGOUT_PATH = "/api/logout"
LOGIN_PATH = "/api/login"
CHECK_PATH = "/api/check"


class AuthTests(TestCase):

    def setUp(self) -> None:
        user1 = User.objects.create(username="user1")
        user1.set_password("")
        user1.save()
        user2 = User.objects.create(username="user2")
        user2.set_password("password2")
        user2.save()

    def test_login_correct(self) -> None:
        """
        Tests that the login endpoint returns a 204 status code and a session
        cookie when the login is successful.
        """
        response = self.client.post(LOGIN_PATH, {"username": "user1"},
                                    content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(len(response.cookies["sessionid"].value) > 0)

        response = self.client.post(LOGIN_PATH, {"username": "user2", "password": "password2"},
                                    content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(len(response.cookies["sessionid"].value) > 0)

    def test_login_incorrect(self) -> None:
        """
        Tests that the login endpoint returns a 401 status code when the login
        is unsuccessful.
        """
        response = self.client.post(LOGIN_PATH, {"username": "user1", "password": "wrong"},
                                    content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 401)

        response = self.client.post(LOGIN_PATH, {"username": "user2"},
                                    content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(LOGIN_PATH, {"username": "wrong"},
                                    content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 401)

        response = self.client.post(LOGIN_PATH)
        self.assertEqual(response.status_code, 400)

    def test_logout(self) -> None:
        """
        Tests that the logout endpoint returns a 204 status code when the user
        is logged in and a 401 status code when the user is not logged in.
        """
        self.client.post(LOGOUT_PATH)  # Logout due to login in SetUp

        response = self.client.post(LOGOUT_PATH)
        self.assertEqual(response.status_code, 401)

        self.client.login(username="user1", password="")

        response = self.client.post(LOGOUT_PATH)
        self.assertEqual(response.status_code, 204)
        response = self.client.post(CHECK_PATH)
        self.assertEqual(response.status_code, 401)

    def test_check(self) -> None:
        """
        Tests that the check endpoint returns a 204 status code when the user is
        logged in and a 401 status code when the user is not logged in.
        """
        self.client.get(LOGOUT_PATH)  # Logout due to login in SetUp

        response = self.client.get(CHECK_PATH)
        self.assertEqual(response.status_code, 401)

        self.client.login(username="user1", password="")

        response = self.client.get(CHECK_PATH)
        self.assertEqual(response.status_code, 204)
