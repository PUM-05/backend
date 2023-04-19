from api.models import Category, Case
from django.db.models import Sum
from datetime import datetime, timedelta
from .cases import get_case_categories
from typing import List, Dict


def get_medium_count(start_time: datetime, end_time: datetime) -> Dict:
    num_email_cases = Case.objects.filter(
        created_at__gte=start_time, created_at__lte=end_time, medium="email").count()
    num_phone_cases = Case.objects.filter(
        created_at__gte=start_time, created_at__lte=end_time, medium="phone").count()

    return {"phone": num_phone_cases, "email": num_email_cases}


def get_stats_per_category(start_time: datetime, end_time: datetime) -> Dict:
    categories = get_case_categories()
    stats = gather_stats_per_category(categories, start_time, end_time)
    return stats


def gather_stats_per_category(categories: List[Dict], start_time: datetime, end_time: datetime) -> List[Dict]:
    result = []
    time_fields = {"customer_time": 0, "additional_time": 0, "form_fill_time": 0}
    for category in categories:
        stat = {"category_id":category["id"], "category_name":category["name"]}

        cases = Case.objects.filter(created_at__gte=start_time, created_at__lte=end_time,
                                    category_id=category["id"])
        stat["count"] = cases.count()

        for key in time_fields:
            time_sum = cases.aggregate(sum=Sum(key))["sum"]
            if time_sum is not None:
                time_fields[key] = time_sum.total_seconds()
            stat[key] = time_fields[key]

        if category.get("subcategories") is not None:
            stat["subcategories"] = gather_stats_per_category(category["subcategories"], start_time, end_time)
            for substat in stat["subcategories"]:
                stat["count"] += substat["count"]
                for key in time_fields:
                    time_fields[key] += stat.get(key)

        result.append(stat)

    return result


def get_stats_per_day(start_time: datetime, delta: timedelta, time_periods: int) -> Dict:
    dates = []
    for i in range(time_periods):
        start = start_time + delta*i
        end = start + delta
        if delta.seconds < 0:
            num_cases = Case.objects.filter(created_at__gte=end, created_at__lte=start).count()
        else:
            num_cases = Case.objects.filter(created_at__gte=start, created_at__lte=end).count()
        stat = {"start":start.isoformat(), "end":end.isoformat(), "count":num_cases}
        dates.append(stat)

    return dates
