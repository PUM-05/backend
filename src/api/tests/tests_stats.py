from datetime import timedelta
from django.test import TestCase
from api.models import Category, Case
from datetime import datetime, timezone


class StatsTests(TestCase):

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

        urls = {url_begin + start + "&end-time=" + end: 200,
                url_begin + late_start + "&end-time=" + new_end: 200,
                url_begin + "incorrect" + "&end-time=" + end: 400,
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
                "/api/stats/periods?incorrect=" + start + "&delta=" + delta + "&intervals=7": 400}

        for url in urls:
            response = self.client.get(url.replace("+", "%2B"))
            self.assertEqual(response.status_code, urls[url])
