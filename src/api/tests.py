import time
from datetime import timedelta
import json
from django.test import TestCase
from api.models import Category, Case
from django.contrib.auth.models import User
from datetime import datetime, timezone

CASE_PATH = "/api/case"
CONTENT_TYPE_JSON = "application/json"
LOGOUT_PATH = "/api/logout"
LOGIN_PATH = "/api/login"
CHECK_PATH = "/api/check"


class APITests(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name="test1")
        Category.objects.create(name="test2")
        Category.objects.create(name="test3")
        Category.objects.create(name="test4")
        p = Category.objects.create(name="test5")
        Category.objects.create(name="test51", parent=p)
        Category.objects.create(name="test52", parent=p)

        Case.objects.create()
        Case.objects.create(medium="phone", form_fill_time=timedelta(seconds=5.3))
        Case.objects.create(medium="email", form_fill_time=timedelta(seconds=10),
                            additional_time=timedelta(seconds=20), notes="This is a note.",
                            customer_time=timedelta(seconds=90), category_id=3)

        Case.objects.create(medium="email", form_fill_time=timedelta(seconds=10),
                            additional_time=timedelta(seconds=20), notes="This is a note.",
                            customer_time=timedelta(seconds=90), category_id=3)

        Case.objects.create(medium="phone", form_fill_time=timedelta(seconds=10),
                            additional_time=timedelta(seconds=20),
                            notes="Johannes did nothing wrong.",
                            customer_time=timedelta(seconds=90), category_id=6)

        user1 = User.objects.create(username="user1")
        user1.set_password("")
        user1.save()
        user2 = User.objects.create(username="user2")
        user2.set_password("password2")
        user2.save()

        # Login required to create cases
        self.client.login(username="user1", password="")

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
        self.client.post(LOGOUT_PATH)   # Logout due to login in SetUp

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

    def test_create_case_correct(self) -> None:
        """
        Test the endpoint for creating a case in the system with correct input values. Iterates 10
        times, each time creating a case with different input parameters and asserts that the
        response status code is 201, indicating that the case was created successfully.
        """
        for i in range(10):
            notes = "notes" + str(i)
            medium = "email" if i % 2 else "phone"
            customer_time = i
            form_fill_time = i
            additional_time = i + 1
            category = (i % 5) + 1
            case_id = i
            dictionary = {"notes": notes, "medium": medium, "customer_time": customer_time,
                          "form_fill_time": form_fill_time, "additional_time": additional_time,
                          "category_id": category, "case_id": case_id}

            response = self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

            self.assertEqual(response.status_code, 201)

    def test_create_case_incorrect_category(self) -> None:
        """
        Test the case creation API endpoint with an incorrect category ID. Sends a
        POST request to the API with a dictionary containing a set of values, including an incorrect
        category ID, and asserts that the response status code is 400, indicating a bad request.
        """
        category = 945
        notes = "notes"
        medium = "email"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

        self.assertEqual(response.status_code, 400)

    def test_create_case_incorrect_medium(self) -> None:
        """
        Test the case creation API endpoint with an incorrect medium value. Sends a POST request to
        the case creation API endpoint with a dictionary that contains an incorrect medium value and
        checks if the response status code is 400, indicating that the request was unsuccessful due
        to a bad request.
        """
        category = 5
        notes = "notes"
        medium = "tiktok"
        dictionary = {"notes": notes, "medium": medium, "category_id": category}

        response = self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

        self.assertEqual(response.status_code, 400)

    def test_get_case_without_parameters(self) -> None:
        """
        Tests that cases are returned and in the correct order with correct status code.
        """
        response = self.client.get(CASE_PATH)
        content = response.content.decode()
        data = json.loads(content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["result_count"], 5)
        self.assertEqual(data["cases"][4]["medium"], None)
        self.assertEqual(data["cases"][3]["medium"], "phone")
        self.assertEqual(data["cases"][2]["medium"], "email")
        self.assertEqual(data["cases"][0]["notes"], "Johannes did nothing wrong.")

    def test_get_case_with_parameters(self) -> None:
        """
        Tests that the correct amount of cases are returned from a set of queries,
        as well as getting the correct status codes.
        """
        # Case.objects.create(medium="email", category_id=3) <- i setUp
        Case.objects.create(medium="email", category_id=3)
        Case.objects.create(medium="email", category_id=3)
        Case.objects.create(medium="email", category_id=2)
        Case.objects.create(medium="email", category_id=2)
        Case.objects.create(medium="email", category_id=2)
        # Case.objects.create(medium="phone") <- i setUp
        Case.objects.create(medium="phone", category_id=3)
        Case.objects.create(medium="phone", category_id=3)
        Case.objects.create(medium="phone", category_id=2)
        Case.objects.create(medium="phone", category_id=2)
        Case.objects.create(medium="phone", category_id=2)

        parameters = {
            "?id=1": 1,
            "?category-id=2": 6,
            "?medium=email": 7,
            "?medium=email&category-id=2": 3,
            "?time-start=2019-01-01 00:00:00Z": 15,
            "?time-end=2024-02-02 00:00:00Z": 15,
            "?per-page=2": 2,
            "?per-page=0": 15,
            "?id=87": 0,
            "?category-id=hej": -1,
            "?category-id=12": -1,
            "?invalid-param=abc": -1,
            "?per-page=hej": -1,
            "?time-end=2019-02-02 00:00:00Z": 0,
            "?time-start=2019-01-01 00:00:00Z&time-end=2018-01-01 00:00:00Z": 0,
        }

        for param in parameters:
            response = self.client.get(CASE_PATH+param)
            content = response.content.decode()
            if parameters[param] == -1:
                # -1 indicates that status 400 should be returned
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 200)
                data = json.loads(content)
                self.assertEqual(data["result_count"], parameters[param])
                self.assertEqual(data["result_count"], len(data["cases"]))

    def test_patch_case(self) -> None:
        """
        Test the ability to update a case using PATCH request. Tests that the endpoint returns 204
        when successful, and that the note field is updated correctly in the database. Also tests
        that a 404 is returned when attempting to update a non-existing case, and that a 400 error
        is returned when trying to update a case with an invalid field or value.
        """
        dictionary = {"notes": "new notes"}

        response = self.client.patch(CASE_PATH + "/1", dictionary, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Case.objects.get(id=1).notes, "new notes")

        response = self.client.patch(CASE_PATH + "/99", dictionary, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 404)

        dictionary = {"medium": "wrong"}
        response = self.client.patch(CASE_PATH + "/1", dictionary, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 400)
        dictionary = {"wrong": "medium"}
        response = self.client.patch(CASE_PATH + "/1", dictionary, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 400)

    def test_nested_categories(self) -> None:
        """
        Tests nested categories by sending a GET request to the "/api/case/categories" endpoint
        and verifying that the response status code is 200. Then it parses the JSON content
        of the response and iterates over all categories and their subcategories, asserting that
        their "id" and "name" attributes are valid.
        """
        response = self.client.get("/api/case/categories")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        data = json.loads(content)
        count = 0
        for category in data:
            count += 1
            self.assertIsNotNone(category["id"])
            self.assertIsNotNone(category["name"])

            for subcategory in category["subcategories"]:
                count += 1
                self.assertIsNotNone(subcategory["id"])
                self.assertIsNotNone(subcategory["name"])
                self.assertFalse("subcategories" in subcategory)

        self.assertEqual(count, 7)

    def test_delete_case_correct_id(self) -> None:
        """
        Tests that the check endpoint returns a 204 status code when a case is found
        and deleted, as well as if the number of cases have changed and if querying a
        deleted object will result in an error.
        """
        no_cases_before = len(Case.objects.all())

        response = self.client.delete(CASE_PATH + "/1", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 204)

        no_cases_after = len(Case.objects.all())
        self.assertEqual(no_cases_before, no_cases_after+1)

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
        response = self.client.delete(CASE_PATH + "/864", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 404)
        response = self.client.delete(CASE_PATH + "/", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 404)

        no_cases_after = len(Case.objects.all())
        self.assertEqual(no_cases_before, no_cases_after)

    def test_case_created_by_and_edited_by(self) -> None:
        """
        Tests if we save the user who created a case correctly in the database and also if
        we correctly save the list of users who has edited the case.
        """
        # --- Login "user1" to create a case done in SetUp ---
        note = "This note is used to test created by and edited by."
        dictionary = {"notes": note}
        self.client.post(CASE_PATH, dictionary, content_type=CONTENT_TYPE_JSON)

        # --- Find the ID of the case we just created ---
        cases = Case.objects.all()
        case_id = None
        for case in cases:
            if case.notes == note:
                case_id = case.id
        test_case = Case.objects.get(id=case_id)

        # --- Login "user2" to edit the case we just created ---
        self.client.login(username="user2", password="password2")
        dictionary = {"notes": "it works!"}
        self.client.patch(CASE_PATH + f"/{case_id}", dictionary, content_type=CONTENT_TYPE_JSON)

        # --- Get a list of all users that have edited the case ---
        edited_by = []
        for user in test_case.edited_by.all():
            edited_by.append(user)

        # --- Check if the case was created by "user1" ---
        created_by_username = str(test_case.created_by)
        self.assertEqual(created_by_username, "user1")

        # --- Check if the case only has been edited by one user and that it is "user2" ---
        edited_by_username = str(edited_by[0])
        self.assertEqual(len(edited_by), 1)
        self.assertEqual(edited_by_username, "user2")

    def test_count_medium(self) -> None:
        """
        Tests the API endpoint /api/stats/medium by making various requests with different
        parameters to the endpoint with various inputs and asserting that the response status code
        is as expected.
        """
        end = (datetime.now(timezone.utc)).isoformat()
        start = (datetime.fromisoformat(end) - timedelta(days=7)).isoformat()
        url_begin = "/api/stats/medium?start-time="

        urls = {url_begin + start + "&end-time=" + end: 200,
                url_begin + "hallå" + "&end-time=" + end: 400,
                url_begin + start + "&end-time=" + "18": 400,
                "/api/stats/medium?time-is-starting=" + start + "&end-time=" + end: 400}

        for url in urls:
            response = self.client.get(url.replace("+", "%2B"))
            self.assertEqual(response.status_code, urls[url])

    def test_stats_per_category(self) -> None:
        """
        Tests the API endpoint /api/stats/category by making various requests with different
        parameters to the endpoint with various inputs and asserting that the response status code
        is as expected.
        """
        end = (datetime.now(timezone.utc)).isoformat()
        start = (datetime.fromisoformat(end) - timedelta(days=7)).isoformat()
        new_end = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        late_start = (datetime.fromisoformat(new_end) + timedelta(days=7)).isoformat()
        url_begin = "/api/stats/category?start-time="

        urls = {url_begin + start + "&end-time=" + end: 200,
                url_begin + late_start + "&end-time=" + new_end: 200,
                url_begin + "test" + "&end-time=" + end: 400,
                "/api/stats/category?time-is-starting=" + start + "&end-time=" + end: 400}

        for url in urls:
            response = self.client.get(url.replace("+", "%2B"))
            self.assertEqual(response.status_code, urls[url])

    def test_stats_per_day(self) -> None:
        """
        Tests the API endpoint /api/stats/day by making various requests with different
        parameters to the endpoint with various inputs and asserting that the response status code
        is as expected.
        """
        end = (datetime.today() + timedelta(days=2)).astimezone(timezone.utc)
        start = (end - timedelta(days=7)).isoformat()
        delta = str(24 * 60 * 60)
        late_start = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        neg_delta = str(-24 * 60 * 60)
        url_begin = "/api/stats/periods?start-time="

        urls = {url_begin + start + "&delta=" + delta + "&intervals=7": 200,
                url_begin + late_start + "&delta=" + delta + "&intervals=7": 200,
                url_begin + start + "&delta=" + neg_delta + "&intervals=7": 200,
                url_begin + start + "&delta=" + delta + "&intervals=incorrect": 400,
                "/api/stats/periods?wrong=" + start + "&delta=" + delta + "&intervals=7": 400}

        for url in urls:
            response = self.client.get(url.replace("+", "%2B"))
            self.assertEqual(response.status_code, urls[url])
