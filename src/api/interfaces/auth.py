from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest


def login_user(request: HttpRequest) -> bool:
    """
    Attempts to log in the user with the username and password provided in the request.
    If successful, the session is updated to keep the user logged in.

    Returns True if the login was successful, otherwise False.
    """
    if "username" in request.POST:
        username = request.POST['username']
    else:
        raise ValueError("Missing username")

    if "password" in request.POST:
        password = request.POST['password']
    else:
        # Use an empty password if none is provided
        password = ""

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return True
    else:
        return False


def logout_user(request: HttpRequest) -> None:
    """
    Logs out the current user.
    """
    logout(request)
