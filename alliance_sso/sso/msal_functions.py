import msal
import uuid

__all__ = [
    "_load_cache",
    "_save_cache",
    "_build_msal_app",
    "_build_auth_url",
    "_get_token_from_cache",
]


def _load_cache(request):
    cache = msal.SerializableTokenCache()
    if request.session.get("sso_token_cache"):
        cache.deserialize(request.session.get("sso_token_cache", None))
    return cache


def _save_cache(request, cache):
    if cache.has_state_changed:
        request.session["sso_token_cache"] = cache.serialize()


def _build_msal_app(request, cache=None, authority=None):
    client_id = request.registry.settings.get("client_id", None)
    authority_name = request.registry.settings.get("authority", None)
    client_secret = request.registry.settings.get("client_secret", None)
    return msal.ConfidentialClientApplication(
        client_id,
        authority=authority or authority_name,
        client_credential=client_secret,
        token_cache=cache,
    )


def _build_auth_url(request, authority=None, scopes=None, state=None):
    return _build_msal_app(request, authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=request.route_url("authorized"),
    )


def _get_token_from_cache(request, scope=None):
    cache = _load_cache(request)  # This web app maintains one cache per session
    cca = _build_msal_app(request, cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(request, cache)
        return result
