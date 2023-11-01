import uuid
from pyramid.httpexceptions import HTTPFound
from .msal_functions import *
from formshare.processes.db.user import get_user_id_with_email, update_last_login
from ast import literal_eval
from formshare.config.auth import get_user_data


def sso_login(request):
    policy = get_policy("main", request)
    login_data = policy.authenticated_userid(request)
    if login_data is not None:
        login_data = literal_eval(login_data)
        if login_data["group"] == "mainApp":
            current_user = get_user_data(login_data["login"], request)
            if current_user is not None:
                next_page = request.params.get("next") or request.route_url(
                    "dashboard", userid=current_user.login
                )
                return HTTPFound(
                    location=next_page,
                )

    scope = request.registry.settings.get("scope", None)
    token = _get_token_from_cache(request, [scope])
    if not token:
        request.session["sso_state"] = str(uuid.uuid4())
        scope = request.registry.settings.get("scope", None)
        auth_url = _build_auth_url(
            request, scopes=[scope], state=request.session["sso_state"]
        )
        return {"auth_url": auth_url}
    else:
        next_page = request.params.get("next") or request.route_url(
            "dashboard", userid=request.session["sso_user"]
        )

        return HTTPFound(location=next_page)


def get_policy(policy_name, request):
    policies = request.policies()
    for policy in policies:
        if policy["name"] == policy_name:
            return policy["policy"]
    return None


def sso_log_out_view(request):
    policy = get_policy("main", request)
    login_data = policy.authenticated_userid(request)
    if login_data is not None:
        login_data = literal_eval(login_data)
        if login_data["group"] == "mainApp":
            headers = policy.forget(request)
            loc = request.route_url("home")
            raise HTTPFound(location=loc, headers=headers)

    request.session.pop("sso_user", None)
    request.session.pop("sso_state", None)
    request.session.pop("sso_token_cache", None)
    authority_name = request.registry.settings.get("authority", None)
    return HTTPFound(
        authority_name
        + "/oauth2/v2.0/logout"
        + "?post_logout_redirect_uri="
        + request.route_url("home")
    )


def sso_authorized(request):
    _ = request.translate
    if request.params.get("state", None) != request.session.get("sso_state"):
        return HTTPFound(request.route_url("login"))
    if "error" in request.params:  # Authentication/Authorization failure
        request.session.flash(_("Error while authorizing your credentials"))
        return HTTPFound(request.route_url("login"))
    if request.params.get("code"):
        cache = _load_cache(request)
        scope = request.registry.settings.get("scope", None)
        result = _build_msal_app(
            request, cache=cache
        ).acquire_token_by_authorization_code(
            request.params["code"],
            scopes=[scope],  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=request.route_url("authorized"),
        )
        if "error" in result:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))
            request.session.flash(_("Error while authorizing your credentials"))
            return HTTPFound(request.route_url("login"))
        sso_user_account = result.get("id_token_claims").get("preferred_username", None)
        if sso_user_account is None:
            return HTTPFound(request.route_url("login"))
        sso_user_account = sso_user_account.lower()
        request.session["sso_user"] = get_user_id_with_email(request, sso_user_account)
        if request.session["sso_user"] is None:
            request.session.flash(
                _(
                    "Your user account hasn't been registered in FormShare. Contact the FormShare administrator"
                )
            )
            return HTTPFound(request.route_url("login"))
        _save_cache(request, cache)
        # print(result.get("id_token_claims"))
        update_last_login(request, request.session["sso_user"])
        return HTTPFound(
            request.route_url("dashboard", userid=request.session["sso_user"])
        )
    else:
        return HTTPFound(request.route_url("login"))
