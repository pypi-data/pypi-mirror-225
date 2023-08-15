from typing import Optional

from django.http import HttpRequest
from django.apps import apps
from django.conf import settings

from ..utils.exceptions import AuthError
from .authenticate_with_username import authenticate_with_username
from .authenticate_with_email import authenticate_with_email
from .authenticate_with_oauth import authenticate_with_oauth

User = apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)


def authenticate(
    password: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    request: Optional[HttpRequest] = None
) -> User:
    if username is None and email is None:
        raise AuthError(message='Email or username is required for authentication', code='EMAIL_USERNAME_MISSING')
    if email is not None:
        user = authenticate_with_email(email=email, password=password, request=request)
    else:
        user = authenticate_with_username(username=username, password=password, request=request)
    return user


__all__ = [
    'authenticate_with_username',
    'authenticate_with_email',
    'authenticate_with_oauth',
    'authenticate'
]
