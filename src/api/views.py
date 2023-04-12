from django.http import HttpResponse, HttpRequest, QueryDict
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
import json
from json.decoder import JSONDecodeError
from .decorators import authentication_required

from api.models import Case

from .interfaces import cases, auth


def login(request: HttpRequest) -> HttpResponse:
    """
    Attempts to log in the user with the given username and password.
    """
    try:
        success = auth.login_user(request)
    except ValueError as error:
        return HttpResponse(status=400, content=str(error))
    except auth.PasswordNeededError as error:
        return HttpResponse(status=403, content=str(error))

    if success:
        return HttpResponse(status=204)
    else:
        error_msg = "Wrong username or password."
        return HttpResponse(status=401, content=error_msg)


def logout(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user.
    """
    if request.user.is_authenticated:
        auth.logout_user(request)
        return HttpResponse(status=204)
    else:
        error_msg = "User is already logged out."
        return HttpResponse(status=401, content=error_msg)


def check(request: HttpRequest) -> HttpResponse:
    """
    Checks if the user is logged in.
    """
    if request.user.is_authenticated:
        return HttpResponse(status=204)
    else:
        error_msg = "User is not logged in."
        return HttpResponse(status=401, content=error_msg)


@authentication_required
@require_http_methods({"GET", "POST"})
def case(request: HttpRequest, str_params="") -> HttpResponse:
    """
    GET: Returns all cases that match the query parameters.
    POST: Creates a new case based on data passed in the request body.
    """
    params = {}
    if str_params:
        params = QueryDict(str_params).dict()
    if request.method == "GET":
        try:
            matching_cases = cases.get_cases(params)
        except ValueError as error:
            return HttpResponse(status=400, content=str(error))

        cases_json = json.dumps(matching_cases, cls=DjangoJSONEncoder)
        print(f"\nparams: {str_params}\ncases: {cases_json}\n")
        return HttpResponse(cases_json, content_type="application/json", status=200)

    elif request.method == "POST":
        try:
            json_string = request.body.decode()
            dictionary = json.loads(json_string)

            new_case = cases.create_case(dictionary)
            new_case.created_by = request.user
            new_case.save()

        except (JSONDecodeError, UnicodeDecodeError, ValueError) as error:
            return HttpResponse(status=400, content=str(error))

        return HttpResponse(status=201)


@authentication_required
@require_http_methods({"PATCH", "DELETE"})
def case_id(request: HttpRequest, id: int) -> HttpResponse:
    """
    PATCH: Updates the case with the given ID based on data passed in the request body.
    DELETE: Deletes the case with the given ID.
    """
    if request.method == "PATCH":
        try:
            json_string = request.body.decode()
            dictionary = json.loads(json_string)

            updated_case = cases.update_case(id, dictionary)
            updated_case.edited_by.add(request.user)
            updated_case.save()

        except (JSONDecodeError, UnicodeDecodeError, ValueError) as error:
            return HttpResponse(status=400, content=str(error))
        except Case.DoesNotExist as error:
            return HttpResponse(status=404, content=str(error))

        return HttpResponse(status=204)

    elif request.method == "DELETE":
        try:
            cases.delete_case(id)
        except Case.DoesNotExist as error:
            return HttpResponse(status=404, content=str(error))
        return HttpResponse(status=204)


@require_http_methods({"GET"})
def case_categories(request: HttpRequest) -> HttpResponse:
    """
    Returns all case categories as a JSON array.
    """
    categories_json = json.dumps(cases.get_case_categories())
    return HttpResponse(categories_json, content_type="application/json", status=200)
