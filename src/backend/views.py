import mimetypes
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render


def static_files(request: HttpRequest) -> HttpResponse:
    """
    Returns the static file at the given path, or the index.html file when appropriate.
    """
    path = request.path

    print("AAAAA" + path)

    if should_return_index(path):
        return render(request, 'index.html')

    else:
        try:
            static_path = path[1:]
            file = open('src/static/' + static_path, 'rb')
        except FileNotFoundError:
            return HttpResponse(status=404)

        type = mimetypes.guess_type(path)[0]

        return FileResponse(file, content_type=type)


def should_return_index(path: str) -> bool:
    """
    Returns true if the given path should return the index.html file.
    """
    return path == "/" or path == "/index.html" or '.' not in path
