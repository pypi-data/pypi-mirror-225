from typing import Optional

from django.apps import apps
from django.conf import settings

from ..utils import validate_email
from .oauth.utils import OAuthClientConfiguration, OAuthTokenResponse
from .oauth.handler import OAuthHandler

User = apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)


class OAuthAuthenticationResponse:
    def __init__(self, user_info: dict, token: OAuthTokenResponse, user: Optional[User]):
        self.user: Optional[User] = user
        self.token: OAuthTokenResponse = token
        self.user_info: dict = user_info

    def __repr__(self):
        return f"<OAuthTokenResponse {self.user_info['email']}>"


def authenticate_with_oauth(
    authorization_code: str,
    client: OAuthClientConfiguration,
) -> OAuthAuthenticationResponse:
    handler = OAuthHandler(client=client)
    result = handler.perform_login(code=authorization_code)
    email = result.email

    try:
        user = User.objects.get(email__iexact=validate_email(email))
    except User.DoesNotExist:
        user = None

    return OAuthAuthenticationResponse(
        user_info=result.user_info,
        token=result.token,
        user=user
    )


__all__ = [
    'authenticate_with_oauth'
]
