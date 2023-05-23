from datetime import timedelta
from django.test import TestCase
from api.models import Category, Case
from datetime import datetime, timezone
import json


class StatsTests(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name="stat_category1")
        Category.objects.create(name="stat_category2")
        p = Category.objects.create(name="stat_category3")
        Category.objects.create(name="stat_subcategory31", parent=p)
        Category.objects.create(name="stat_subcategory32", parent=p)

        Case.objects.create(medium="phone",
                            additional_time=timedelta(seconds=20),
                            customer_time=timedelta(seconds=50),
                            form_fill_time=timedelta(seconds=10),
                            category_id=2)
        Case.objects.create(medium="phone",
                            additional_time=timedelta(seconds=30),
                            customer_time=timedelta(seconds=50),
                            form_fill_time=timedelta(seconds=20),
                            category_id=2)
        Case.objects.create(medium="phone",
                            customer_time=timedelta(seconds=40),
                            form_fill_time=timedelta(seconds=30),
                            category_id=4)
        Case.objects.create(medium="phone",
                            customer_time=timedelta(seconds=160),
                            category_id=5)

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
                url_begin + "incorrect" + "&end-time=" + end: 400,
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

        urls = {url_begin + late_start + "&end-time=" + new_end: 200,
                url_begin + "incorrect" + "&end-time=" + end: 400,
                "/api/stats/category?time-is-starting=" + start + "&end-time=" + end: 400}
        for url in urls:
            response = self.client.get(url.replace("+", "%2B"))
            self.assertEqual(response.status_code, urls[url])

        url = url_begin + start + "&end-time=" + end
        response = self.client.get(url.replace("+", "%2B"))
        content = response.content.decode()
        data = json.loads(content)
        self.assertEqual(data[0]["customer_time"], 0)
        self.assertEqual(data[0]["additional_time"], 0)
        self.assertEqual(data[0]["form_fill_time"], 0)
        self.assertEqual(data[1]["customer_time"], 100)
        self.assertEqual(data[1]["additional_time"], 50)
        self.assertEqual(data[2]["customer_time"], 200)
        self.assertEqual(data[2]["subcategories"][0]["customer_time"], 40)
        self.assertEqual(data[2]["subcategories"][1]["customer_time"], 160)
        self.assertEqual(response.status_code, 200)

    def test_stats_per_period(self) -> None:
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
                "/api/stats/periods?incorrect=" + start + "&delta=" + delta + "&intervals=7": 400}

        for url in urls:
            response = self.client.get(url.replace("+", "%2B"))
            self.assertEqual(response.status_code, urls[url])

        response = self.client.get(
            "/api/stats/periods?start-time=2000-01-01T00:00:00%2B00:00&delta=9999999999&intervals=1"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data[0]["count"], 4)
        self.assertEqual(data[0]["total_form_fill_time"], 60)
