from datetime import timedelta
from typing import Any, Dict, List
from django.db.models import Q
from api.models import Category, Case


def get_cases(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns all cases that match the given parameters.
    """
    valid_params = {"id", "case-id", "time-start", "time-end", "category-id", "medium", "per-page",
                    "page"}

    params = {
        "id": "id",
        "case-id": "case_id",
        "time-start": "created_at__gte",
        "time-end": "created_at__lte",
        "medium": "medium",
    }

    for param in parameters:
        if param not in valid_params:
            raise ValueError(f"Unexpected parameter: {param}={parameters[param]}.")

    # Builds a query using dict comprehension, which is basically like a mapping function. It
    # creates a set of queries from the key-value pairs in parameters with the individual queries
    # looking like "params[key]=value". Only the key-value pairs where key is in params are
    # included.
    query = Q(**{params[k]: v for k, v in parameters.items() if k in params.keys()})

    if "category-id" in parameters:
        try:
            category = Category.objects.get(id=parameters["category-id"])
        except Category.DoesNotExist:
            raise ValueError(f"Category id={parameters['category-id']} does not exist")
        query &= Q(category=category)

    per_page = int(parameters.get("per-page", 100))
    page = int(parameters.get("page", 1))
    start = per_page * (page - 1)
    end = per_page * page

    if per_page != 0:
        result = list(Case.objects.filter(query)[start:end + 1].values())
        has_more = len(result) == per_page + 1
    else:
        result = list(Case.objects.filter(query).values())
        has_more = False

    for case in result:
        # Change all datetimes to seconds and add category name
        keys = ["additional_time", "form_fill_time", "customer_time"]
        try:
            case["category_name"] = Category.objects.get(id=case["category_id"]).name
        except Category.DoesNotExist:
            case["category_name"] = None
        for key in keys:
            if case[key] is not None:
                case[key] = case[key].total_seconds()

    result_count = len(result)

    if has_more:
        result_count -= 1
        result = result[:-1]

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
    list_of_keys = {"notes", "medium", "customer_time", "additional_time",
                    "form_fill_time", "category_id", "case_id"}
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

    if "case_id" in dictionary:
        case.case_id = dictionary.get("case_id")

    if "customer_time" in dictionary:
        case.customer_time = timedelta(seconds=dictionary["customer_time"] or 0)

    if "additional_time" in dictionary:
        case.additional_time = timedelta(seconds=dictionary["additional_time"] or 0)

    if "form_fill_time" in dictionary:
        case.form_fill_time = timedelta(seconds=dictionary["form_fill_time"] or 0)

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
