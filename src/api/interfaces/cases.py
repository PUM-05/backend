from typing import Any, Dict, List


# TODO: Return type should be list of case models when they are implemented
def get_case(parameters: Dict[str, Any]):
    """
    Returns all cases that match the given parameters.
    """
    # Return dummy data
    return [{"id": 1, "medium": "phone", "notes": "Hello World!"},
            {"id": 2, "medium": "email", "notes": "This is a test."}]


# TODO: Return type should be list of category models when they are implemented
def get_case_categories() -> List[Dict[str, Any]]:
    """
    Returns all case categories.
    """
    # Return dummy data
    return [{"id": 1, "name": "category1"},
            {"id": 2, "name": "category2"},
            {"id": 3, "name": "category3"},
            {"id": 4, "name": "category4"}]