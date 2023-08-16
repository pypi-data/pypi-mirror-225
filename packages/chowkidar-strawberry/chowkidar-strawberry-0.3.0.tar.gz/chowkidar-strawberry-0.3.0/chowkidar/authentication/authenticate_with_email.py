from typing import Optional

from django.http import HttpRequest
from django.apps import apps
from django.conf import settings

from ..utils import validate_email
from ..utils.exceptions import AuthError
from .authenticate_with_username import authenticate_with_username

User = apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)


def authenticate_with_email(password: str, email: str, request: Optional[HttpRequest] = None) -> User:
    try:
        username = User.objects.get(email__iexact=validate_email(email)).username
        return authenticate_with_username(password=password, username=username, request=request)
    except User.DoesNotExist:
        raise AuthError(message='An account with this email address does not exist', code='EMAIL_NOT_FOUND')
    except User.MultipleObjectsReturned:
        raise AuthError(
            message='We cannot authenticate you with your email address, please enter your username',
            code='EMAIL_NOT_UNIQUE'
        )


__all__ = [
    'authenticate_with_email'
]
