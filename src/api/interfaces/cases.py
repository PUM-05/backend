from datetime import timedelta
import datetime
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

    case.notes = dictionary["notes"]
    case.medium = dictionary["medium"]
    case.customer_time = timedelta(seconds=dictionary["customer_time"] or 0)
    case.additional_time = timedelta(seconds=dictionary["additional_time"] or 0)
    case.form_fill_time = timedelta(seconds=dictionary["form_fill_time"] or 0)
    case.created_at = datetime.now()
    case.edited_at = datetime.now()
   
    try:
        category = Category.objects.get(id=dictionary["category_id"])
    except:
        raise ValueError
    
    case.category = category
    case.save()


def get_case_categories() -> List[Dict]:
    """
    Returns all case categories.
    """
    return list(Category.objects.all().values())
