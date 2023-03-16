from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
import json
from json.decoder import JSONDecodeError

from .interfaces import cases, auth


def login(request: HttpRequest) -> HttpResponse:
    """
    Attempts to log in the user with the given username and password.
    """
    try:
        success = auth.login_user(request)
    except ValueError:
        return HttpResponse(status=400)

    if success:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


def logout(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user.
    """
    if request.user.is_authenticated:
        auth.logout_user(request)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


def check(request: HttpRequest) -> HttpResponse:
    """
    Checks if the user is logged in.
    """
    if request.user.is_authenticated:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


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
    Returns all case categories as a JSON array.
    """
    categories_json = json.dumps(cases.get_case_categories())
    return HttpResponse(categories_json, content_type="application/json", status=200)
