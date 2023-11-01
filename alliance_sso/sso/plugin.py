import formshare.plugins as plugins
import formshare.plugins.utilities as u
from .views import sso_login, sso_authorized, sso_log_out_view
import sys
import os
from .msal_functions import _get_token_from_cache
from formshare.views.basic_views import LoginView
from ast import literal_eval


class sso(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IUserAuthorization)
    plugins.implements(plugins.IUserAuthentication)

    # Implements IRoutes
    def before_mapping(self, config):
        # We don't add any routes before the host application
        return []

    def after_mapping(self, config):
        # We add here a new route /json that returns a JSON
        settings = config.get_settings()
        custom_map = [
            u.add_route("login", "/login", sso_login, "generic/login.jinja2"),
            u.add_route("login_normal", "/login_normal", LoginView, None),
            u.add_route(
                "authorized", settings.get("redirect_path"), sso_authorized, None
            ),
            u.add_route("logout", "/logout", sso_log_out_view, None),
        ]

        return custom_map

    # Implements IConfig
    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")

    # Implements ITranslation
    def get_translation_directory(self):
        module = sys.modules["sso"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "sso"

    # Implements IUserAuthorization
    def before_check_authorization(self, request):
        return False

    def get_policy(self, policy_name, request):
        policies = request.policies()
        for policy in policies:
            if policy["name"] == policy_name:
                return policy["policy"]
        return None

    def custom_authorization(self, request):
        scope = request.registry.settings.get("scope", None)
        scopes = [scope]
        token = _get_token_from_cache(request, scopes)
        if not token:
            policy = self.get_policy("main", request)
            login_data = policy.authenticated_userid(request)
            if login_data is not None:
                login_data = literal_eval(login_data)
                if login_data["group"] == "mainApp":
                    return True, login_data["login"]
            return False, ""
        else:
            return True, request.session["sso_user"]

    # IUserAuthentication
    def after_login(self, request, user):
        _ = request.translate
        user_email = user.email
        user_email = user_email.strip()
        user_email = user_email.lower()
        if user_email.find("@cgiar.org") >= 0:
            return False, _(
                'You must use the link "Sign in with your CGIAR account"'
            )
        else:
            return True, ""

    def on_authenticate_user(self, request, user_id, user_is_email):
        return None, {}

    def on_authenticate_password(self, request, user_data, password):
        return None, None
