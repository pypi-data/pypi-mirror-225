from typing import Optional


class OAuthTokenResponse:
    def __init__(self, access_token: str, token_type: str = 'Bearer', refresh_token: str = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type

    def __repr__(self):
        return f"<OAuthTokenResponse {self.access_token}>"


class OAuthLoginResponse:
    def __init__(self, token: OAuthTokenResponse, user_info: dict, email: Optional[str] = None):
        self.token: OAuthTokenResponse = token
        self.user_info = user_info
        self.email = email or user_info['email']

    def __repr__(self):
        return f"<OAuthLoginResponse {self.token} {self.user_info}>"


class OAuthProviderConfiguration:

    def __init__(
        self,
        name: str,
        authorizationEndpoint: str,
        tokenEndpoint: str,
        userInfoEndpoint: str,
        revocationEndpoint: str = None,
        authVar: Optional[str] = "Bearer"
    ):
        self.name = name
        self.authorizationEndpoint = authorizationEndpoint
        self.tokenEndpoint = tokenEndpoint
        self.userInfoEndpoint = userInfoEndpoint
        self.revocationEndpoint = revocationEndpoint
        self.authVar = authVar


class OAuthClientConfiguration:

    def __init__(
        self,
        clientID: str,
        clientSecret: str,
        redirectURI: str,
        provider: OAuthProviderConfiguration,
        scopes: str = None
    ):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.redirectURI = redirectURI
        self.scopes = scopes
        self.provider = provider


__all__ = [
    'OAuthTokenResponse',
    'OAuthLoginResponse',
    'OAuthProviderConfiguration',
    'OAuthClientConfiguration'
]
