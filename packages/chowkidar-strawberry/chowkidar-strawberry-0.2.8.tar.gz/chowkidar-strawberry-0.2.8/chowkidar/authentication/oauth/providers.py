from .utils import OAuthProviderConfiguration

GOOGLE_OAUTH_CONFIG = OAuthProviderConfiguration(
    name='google',
    authorizationEndpoint='https://accounts.google.com/o/oauth2/v2/auth',
    tokenEndpoint='https://oauth2.googleapis.com/token',
    userInfoEndpoint='https://www.googleapis.com/oauth2/v1/userinfo?alt=json',
    authVar='Bearer'
)

GITHUB_OAUTH_CONFIG = OAuthProviderConfiguration(
    name='github',
    authorizationEndpoint='https://github.com/login/oauth/authorize',
    tokenEndpoint='https://github.com/login/oauth/access_token',
    userInfoEndpoint='https://api.github.com/user',
    authVar='token'
)

TWITTER_OAUTH_CONFIG = OAuthProviderConfiguration(
    name='twitter',
    authorizationEndpoint='https://twitter.com/i/oauth2/authorize',
    tokenEndpoint='https://api.twitter.com/oauth2/token',
    userInfoEndpoint='https://api.twitter.com/2/users/me',
    authVar='Bearer'
)

DISCORD_OAUTH_CONFIG = OAuthProviderConfiguration(
    name="discord",
    authorizationEndpoint="https://discord.com/oauth2/authorize",
    tokenEndpoint="https://discord.com/api/oauth2/token",
    userInfoEndpoint="https://discord.com/api/users/@me",
    authVar='Bearer'
)


def get_provider_configuration(provider: str) -> OAuthProviderConfiguration:
    if provider.lower() == 'google':
        return GOOGLE_OAUTH_CONFIG
    elif provider.lower() == 'github':
        return GITHUB_OAUTH_CONFIG
    elif provider.lower() == 'twitter':
        return TWITTER_OAUTH_CONFIG
    elif provider.lower() == 'discord':
        return DISCORD_OAUTH_CONFIG
    else:
        raise ValueError(f'Unknown OAuth provider: {provider}')


__all__ = [
    'GITHUB_OAUTH_CONFIG',
    'GOOGLE_OAUTH_CONFIG',
    'TWITTER_OAUTH_CONFIG',
    'DISCORD_OAUTH_CONFIG',
    'get_provider_configuration',
]
