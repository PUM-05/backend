from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
import json


class PasswordNeededError(Exception):
    pass


def login_user(request: HttpRequest) -> bool:
    """
    Attempts to log in the user with the username and password provided in the request.
    If successful, the session is updated to keep the user logged in.

    Returns True if the login was successful, otherwise False.
    """

    json_string = request.body.decode()
    dictionary = json.loads(json_string)

    if "username" in dictionary:
        username = dictionary['username']
    else:
        raise ValueError("Missing username.")

    if "password" in dictionary:
        password = dictionary['password']
    else:
        # Use an empty password if none is provided
        password = ""

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return True
    else:
        if not password:
            if User.objects.filter(username=username).exists():
                raise PasswordNeededError("Password required.")
        return False


def logout_user(request: HttpRequest) -> None:
    """
    Logs out the current user.
    """
    logout(request)
