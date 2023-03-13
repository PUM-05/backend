from datetime import datetime, timedelta
from typing import Any, Dict, List

from api.models import Category, Case


def get_cases(parameters: Dict[str, Any]) -> List[Dict]:
    """
    Returns all cases that match the given parameters.
    """
    # TODO: Implement parameters
    return list(Case.objects.all().values())


def validate_case(dictionary: Dict) -> bool:
    """
    Returns true if all keys in the given dictionary are valid,
    false otherwise.
    """
    list_of_keys = {"notes", "medium", "customer_time",
                    "additional_time", "form_fill_time", "category_id"}
    for key in dictionary.keys():
        if key not in list_of_keys:
            return False
    return True


def create_case(dictionary: Dict) -> None:
    """
    Creates a new case and adds it to the data base. Raises ValueError if
    the data is incorrect.
    """
    if not validate_case:
        raise ValueError

    case = Case()

    case.notes = dictionary.get("notes")
    case.customer_time = timedelta(seconds=dictionary.get("customer_time") or 0)
    case.additional_time = timedelta(seconds=dictionary.get("additional_time") or 0)
    case.form_fill_time = timedelta(seconds=dictionary.get("form_fill_time") or 0)

    medium = dictionary.get("medium")
    if "medium" in dictionary and (medium != "phone" and medium != "email"):
        raise ValueError

    else:
        case.medium = medium

    if "category_id" in dictionary:
        try:
            category = Category.objects.get(id=dictionary.get("category_id"))
        except Category.DoesNotExist:
            raise ValueError

        case.category = category
    case.save()


def get_case_categories() -> List[Dict]:
    """
    Returns all case categories.
    """
    return list(Category.objects.all().values())
