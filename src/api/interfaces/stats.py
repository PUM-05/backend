from api.models import Category, Case
from datetime import datetime
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
    stats = []
    for category in categories:
        num_cases = Case.objects.filter(created_at__gte=start_time, created_at__lte=end_time,
                                        category_id=category["id"]).count()
        subcategory_stats = []
        if ("subcategories" in category) and (category["subcategories"] is not None):
            subcategories = category["subcategories"]
            subcategory_stats = gather_stats_per_category(subcategories, start_time, end_time)

        category_stat = {"id":category["id"], # input_time? initial_time? extra_time? total_time? what does it all mean?
                         "name":category["name"],
                         "count":num_cases,
                         "subcategories":subcategory_stats}
        stats.append(category_stat)

    return stats
