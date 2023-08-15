from typing import Optional

from django.http import HttpRequest
from django.apps import apps
from django.conf import settings

from ..utils.exceptions import AuthError

User = apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)


def authenticate_with_username(password: str, username: str, request: Optional[HttpRequest] = None) -> User:
    """
    Authenticate user with username and password using django's inbuilt authenticate function
    :param password: raw password of the user
    :param username: username of the user
    :param request: request object (optional)
    :return: User instance
    """
    from django.contrib.auth import authenticate
    user = authenticate(request=request, username=username, password=password)
    if user is None:
        msg = 'The username or password you entered is wrong'
        if username is None:
            msg = 'The email or password you entered is wrong'
        raise AuthError(message=msg, code='INVALID_CREDENTIALS')
    return user


__all__ = [
    'authenticate_with_username'
]
