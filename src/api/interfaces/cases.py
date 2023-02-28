from datetime import datetime, timedelta
from typing import Any, Dict, List

from api.models import Category, Case


# TODO: Return type should be list of case models when they are implemented
def get_case(parameters: Dict[str, Any]):
    """
    Returns all cases that match the given parameters.
    """
    # Return dummy data
    return [{"id": 1, "medium": "phone", "notes": "Hello World!"},
            {"id": 2, "medium": "email", "notes": "This is a test."}]


def create_case(dictionary: Dict):
    case = Case()

    case.notes = dictionary.get("notes")
    case.medium = dictionary.get("medium")
    case.customer_time = timedelta(
        seconds=dictionary.get("customer_time") or 0)
    case.additional_time = timedelta(
        seconds=dictionary.get("additional_time") or 0)
    case.form_fill_time = timedelta(
        seconds=dictionary.get("form_fill_time") or 0)

    if "category_id" in dictionary:
        try:
            category = Category.objects.get(id=dictionary.get("category_id"))
        except:
            raise ValueError

        case.category = category
    case.save()


def get_case_categories() -> List[Dict]:
    """
    Returns all case categories.
    """
    return list(Category.objects.all().values())
