from api.models import Category, Case
from datetime import datetime


def get_medium_count(start_time: datetime, end_time: datetime) -> dict:

    num_email_cases = Case.objects.filter(
        created_at__gte=start_time, created_at__lte=end_time, medium="email").count()
    num_phone_cases = Case.objects.filter(
        created_at__gte=start_time, created_at__lte=end_time, medium="phone").count()

    return {"phone": num_phone_cases, "email": num_email_cases}
