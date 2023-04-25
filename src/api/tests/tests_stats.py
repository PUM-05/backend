from datetime import timedelta
from django.test import TestCase
from api.models import Category, Case
from django.contrib.auth.models import User
from datetime import datetime, timezone


class CasesTests(TestCase):

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
