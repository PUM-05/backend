from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
import json

from api.interfaces.cases import get_case


def example(request):
    return HttpResponse("Hello World!")


@require_http_methods({"GET", "POST"})
def case(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse(json.dumps(get_case()), content_type="application/json")
    
    elif request.method == "POST":
        return HttpResponse()
   

@require_http_methods({"PATCH", "DELETE"})
def case_id(request: HttpRequest, id: int):
    if request.method == "PATCH":
        return HttpResponse()

    elif request.method == "DELETE":
        return HttpResponse()
