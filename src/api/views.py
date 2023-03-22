from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
import json
from json.decoder import JSONDecodeError

from .interfaces import cases


@require_http_methods({"GET", "POST"})
def case(request: HttpRequest) -> HttpResponse:
    """
    GET: Returns all cases that match the query parameters.
    POST: Creates a new case based on data passed in the request body.
    """
    if request.method == "GET":
        params = request.GET.dict()

        try:
            matching_cases = cases.get_cases(params)
        except ValueError:
            return HttpResponse(status=400)

        cases_json = json.dumps(matching_cases, cls=DjangoJSONEncoder)
        return HttpResponse(cases_json, content_type="application/json", status=200)

    elif request.method == "POST":
        try:
            json_string = request.body.decode()
            dictionary = json.loads(json_string)
            cases.create_case(dictionary)

        except (JSONDecodeError, UnicodeDecodeError, ValueError):
            return HttpResponse(status=400)

        return HttpResponse(status=201)


@require_http_methods({"PATCH", "DELETE"})
def case_id(request: HttpRequest, id: int) -> HttpResponse:
    """
    PATCH: Updates the case with the given ID based on data passed in the request body.
    DELETE: Deletes the case with the given ID.
    """
    if request.method == "PATCH":
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        return HttpResponse(status=204)


@require_http_methods({"GET"})
def case_categories(request: HttpRequest) -> HttpResponse:
    """
    Returns all top lvl case categories as a JSON array.
    """
    categories_json = json.dumps(cases.get_case_categories())
    return HttpResponse(categories_json, content_type="application/json", status=200)
