from datetime import datetime, timedelta
from typing import Any, Dict, List
from django.db.models import Q

from api.models import Category, Case


def get_cases(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns all cases that match the given parameters.
    """
    query = Q()
    per_page = 100
    page = 1
    valid_params = {"id", "index-start", "index-end", "time-start", "time-end",
                    "category-id", "medium", "per-page", "page"}

    for param in parameters:
        if param not in valid_params:
            raise ValueError(f"Unexpected parameter: {param}={parameters[param]}.")

    if "id" in parameters:
        query &= Q(id=parameters["id"])

    if "index-start" in parameters:
        query &= Q(id__gte=parameters["index-start"])

    if "index-end" in parameters:
        query &= Q(id__lte=parameters["index-end"])

    if "time-start" in parameters:

        query &= Q(created_at__gte=parameters["time-start"])

    if "time-end" in parameters:
        query &= Q(created_at__lte=parameters["time-end"])

    if "category-id" in parameters:
        try:
            category = Category.objects.get(id=parameters["category-id"])
        except Category.DoesNotExist:
            raise ValueError(f"Category id={parameters['category-id']} does not exist")
        query &= Q(category=category)

    if "medium" in parameters:
        query &= Q(medium=parameters["medium"])

    if "per-page" in parameters:
        per_page = parameters["per-page"]

    if "page" in parameters:
        page = parameters["page"]

    start = per_page * (page - 1)
    end = per_page * page

    result = list(Case.objects.filter(query)[start:end+1].values())
    has_more = len(result) == per_page + 1
    result_count = len(result)

    if has_more:
        result_count = len(result) - 1
        result = result[:-1]

    for case in result:
        # Change all datetimes to seconds
        keys = ["additional_time", "form_fill_time", "customer_time"]

        for key in keys:
            if case[key] is not None:
                case[key] = case[key].total_seconds()

    return {
        "result_count": result_count,
        "has_more": has_more,
        "cases": result,
    }


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


def create_case(dictionary: Dict) -> Case:
    """
    Creates a new case and adds it to the database. Raises ValueError if
    the data is incorrect. Returns the new case.
    """
    validate_case(dictionary)
    case = Case()
    fill_case(case, dictionary)

    return case


def update_case(case_id: int, dictionary: Dict) -> Case:
    """
    Updates a case with a given id. Raises Case.DoesNotExist if wrong case_id,
    and ValueError if the dictionary contains bad data. Returns the edited case.
    """
    validate_case(dictionary)
    case = Case.objects.get(id=case_id)
    fill_case(case, dictionary)

    return case


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
