import mimetypes
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render


def static_files(request: HttpRequest) -> HttpResponse:
    """
    Returns the static file at the given path, or the index.html file when appropriate.
    """
    path = request.path

    if should_return_index(path):
        relative_path = "index.html"
    else:
        relative_path = path[1:]

    try:
        static_file = open("src/static/" + relative_path, "rb")
    except FileNotFoundError:
        return HttpResponse(status=404)

    file_type = mimetypes.guess_type(path)[0]

    return FileResponse(static_file, content_type=file_type)


def should_return_index(path: str) -> bool:
    """
    Returns true if the given path should return the index.html file.
    """
    return path == "/" or path == "/index.html" or '.' not in path
