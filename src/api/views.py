from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
import json
from json.decoder import JSONDecodeError
from .decorators import authentication_required
from api.models import Case
from .interfaces import cases, auth, stats
from datetime import datetime, timedelta

last_cleaned = datetime.today() - timedelta(days=1)


def set_cleaned_for_testing() -> None:
    """
    Sets the last_cleaned variable to a date in the past,
    makes clean_case_notes() run on the next API call for testing.
    """
    global last_cleaned
    last_cleaned = datetime.today() - timedelta(days=2)


def clean_case_notes() -> None:
    """
    Removes notes from cases older than 90 days.
    """
    global last_cleaned
    if datetime.today() > last_cleaned:
        cases.remove_old_notes()
        last_cleaned = datetime.today()


def login(request: HttpRequest) -> HttpResponse:
    """
    Attempts to log in the user with the given username and password.
    """
    clean_case_notes()
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
    clean_case_notes()
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
    clean_case_notes()
    if request.user.is_authenticated:
        return HttpResponse(status=204)
    else:
        error_msg = "User is not logged in."
        return HttpResponse(status=401, content=error_msg)


@authentication_required
@require_http_methods({"GET", "POST"})
def case(request: HttpRequest) -> HttpResponse:
    """
    GET: Returns all cases that match the query parameters.
    POST: Creates a new case based on data passed in the request body.
    """
    clean_case_notes()
    if request.method == "GET":
        try:
            matching_cases = cases.get_cases(request.GET.dict())
        except ValueError as error:
            return HttpResponse(status=400, content=str(error))

        cases_json = json.dumps(matching_cases, cls=DjangoJSONEncoder)
        return HttpResponse(cases_json, content_type="application/json", status=200)

    elif request.method == "POST":
        try:
            json_string = request.body.decode()
            dictionary = json.loads(json_string)

            new_case = cases.create_case(dictionary)
            new_case.created_by = request.user
            new_case.save()

        except (JSONDecodeError, UnicodeDecodeError, ValueError, TypeError) as error:
            return HttpResponse(status=400, content=str(error))

        return HttpResponse(status=201)


@authentication_required
@require_http_methods({"PATCH", "DELETE"})
def case_id(request: HttpRequest, id: int) -> HttpResponse:
    """
    PATCH: Updates the case with the given ID based on data passed in the request body.
    DELETE: Deletes the case with the given ID.
    """
    clean_case_notes()
    if request.method == "PATCH":
        try:
            json_string = request.body.decode()
            dictionary = json.loads(json_string)

            updated_case = cases.update_case(id, dictionary)
            updated_case.edited_by.add(request.user)
            updated_case.save()

        except (JSONDecodeError, UnicodeDecodeError, ValueError, TypeError) as error:
            return HttpResponse(status=400, content=str(error))
        except Case.DoesNotExist as error:
            return HttpResponse(status=404, content=str(error))

        return HttpResponse(status=204)

    elif request.method == "DELETE":
        try:
            cases.delete_case(id)
        except TypeError as error:
            return HttpResponse(status=400, content=str(error))
        except Case.DoesNotExist as error:
            return HttpResponse(status=404, content=str(error))
        return HttpResponse(status=204)


@require_http_methods({"GET"})
def case_categories(request: HttpRequest) -> HttpResponse:
    """
    Returns all case categories as a JSON array.
    """
    clean_case_notes()
    categories_json = json.dumps(cases.get_case_categories())
    return HttpResponse(categories_json, content_type="application/json", status=200)


@require_http_methods({"GET"})
def stats_per_medium(request: HttpRequest) -> HttpResponse:
    """
    Returns the number of cases per medium for a given time range as a JSON array.
    """
    clean_case_notes()
    params = request.GET.dict()
    try:
        start_time_iso = params["start-time"]
        end_time_iso = params["end-time"]
        start_time = datetime.fromisoformat(start_time_iso)
        end_time = datetime.fromisoformat(end_time_iso)

    except KeyError as error:
        return HttpResponse(status=400, content="Key does not exist: " + str(error))

    except ValueError as error:
        return HttpResponse(status=400, content=str(error))

    medium_stats = json.dumps(stats.get_medium_count(start_time, end_time))
    return HttpResponse(medium_stats, content_type="application/json", status=200)


@require_http_methods({"GET"})
def stats_per_category(request: HttpRequest) -> HttpResponse:
    """
    Returns the statistics for cases per category and subcategory for a given time range a JSON
    array.
    """
    clean_case_notes()
    params = request.GET.dict()
    try:
        start_time_iso = params["start-time"]
        end_time_iso = params["end-time"]
        start_time = datetime.fromisoformat(start_time_iso)
        end_time = datetime.fromisoformat(end_time_iso)

    except KeyError as error:
        return HttpResponse(status=400, content="Key does not exist: " + str(error))

    except ValueError as error:
        return HttpResponse(status=400, content=str(error))

    stats_per_category = json.dumps(stats.get_stats_per_category(start_time, end_time))
    return HttpResponse(stats_per_category, content_type="application/json", status=200)


@require_http_methods({"GET"})
def stats_per_period(request: HttpRequest) -> HttpResponse:
    """
    Returns the number of cases per time period for a given interval as a JSON array.
    """
    clean_case_notes()
    params = request.GET.dict()
    try:
        start_time_iso = params["start-time"]
        start_time = datetime.fromisoformat(start_time_iso)
        delta = timedelta(seconds=int(params["delta"]))
        time_periods = int(params["intervals"])

    except KeyError as error:
        return HttpResponse(status=400, content="Key does not exist: " + str(error))

    except ValueError as error:
        return HttpResponse(status=400, content=str(error))

    stats_per_day = json.dumps(stats.get_stats_per_period(start_time, delta, time_periods))
    return HttpResponse(stats_per_day, content_type="application/json", status=200)
