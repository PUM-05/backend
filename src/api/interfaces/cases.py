from datetime import datetime, timedelta
from typing import Any, Dict, List

from api.models import Category, Case


def get_cases(parameters: Dict[str, Any]) -> List[Dict]:
    """
    Returns all cases that match the given parameters.
    """
    # TODO: Implement parameters
    return list(Case.objects.all().values())


def validate_case(dictionary: Dict) -> None:
    """
    Throws ValueError if any key in the given dictionary is invalid,
    otherwise returns None.
    """
    list_of_keys = {"notes", "medium", "customer_time",
                    "additional_time", "form_fill_time", "category_id"}
    for key in dictionary.keys():
        if key not in list_of_keys:
            raise ValueError(f"Unexpected key: {key}.")


def create_case(dictionary: Dict) -> None:
    """
    Creates a new case and adds it to the database. Raises ValueError if
    the data is incorrect.
    """
    validate_case(dictionary)

    case = Case()

    fill_case(case, dictionary)
    case.save()


def update_case(case_id: int, dictionary: Dict) -> None:
    """
    Updates a case with a given id.
    Raises Case.DoesNotExist if wrong case_id,
    and ValueError if the dictionary contains bad data.
    """
    validate_case(dictionary)

    case = Case.objects.get(id=case_id)

    fill_case(case, dictionary)
    case.save()


def fill_case(case: Case, dictionary: Dict) -> None:
    """
    Updates a given case with properties from a given dictionary.
    Raises ValueError if dictionary values are not valid.
    """
    if "notes" in dictionary:
        case.notes = dictionary.get("notes")

    if "customer_time" in dictionary:
        case.customer_time = timedelta(seconds=dictionary.get("customer_time") or 0)

    if "additional_time" in dictionary:
        case.additional_time = timedelta(seconds=dictionary.get("additional_time") or 0)

    if "form_fill_time" in dictionary:
        case.form_fill_time = timedelta(seconds=dictionary.get("form_fill_time") or 0)

    if "medium" in dictionary:
        medium = dictionary.get("medium")
        if medium == "phone" or medium == "email":
            case.medium = medium
        else:
            raise ValueError(f"Invalid medium: {medium}.")

    if "category_id" in dictionary:
        try:
            category = Category.objects.get(id=dictionary.get("category_id"))
        except Category.DoesNotExist:
            raise ValueError(f"Category with id {dictionary.get('category_id')} does not exist.")

        case.category = category


def get_case_categories() -> List[Dict]:
    """
    Returns all case categories.
    """
    categories = []
    indexes = {}
    i = 0
    flat_categories = list(Category.objects.all().values())
    for category in flat_categories:
        if not category["parent_id"]:
            categories.append(
                {"id": category["id"], "name": category["name"], "subcategories": []}
            )
            indexes[category["id"]] = i
            i += 1
        else:
            categories[indexes[category["parent_id"]]]["subcategories"].append(
                {"id": category["id"], "name": category["name"]}
            )

    return categories


def delete_case(case_id: int) -> None:
    """
    Deletes a case with the given id.
    """
    case = Case.objects.get(id=case_id)
    case.delete()
