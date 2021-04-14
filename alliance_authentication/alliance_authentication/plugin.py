import formshare.plugins as plugins
import formshare.plugins.utilities as u
import sys
import os
from subprocess import Popen, PIPE
import logging

log = logging.getLogger("formshare")


class alliance_authentication(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IUserAuthentication)

    # Implements IConfig
    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")

    # Implements ITranslation
    def get_translation_directory(self):
        module = sys.modules["alliance_authentication"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "alliance_authentication"

    # Implements IUserAuthentication
    def after_login(self, request, user):
        return True, ""

    def on_authenticate_user(self, request, user_id, user_is_email):
        return None, {}

    def on_authenticate_password(self, request, user_data, password):
        java_java = request.registry.settings.get("java.authentication.jar")
        args = ["java", "-jar", java_java]
        if (
            request.registry.settings.get("java.authentication.remote", "false")
            == "true"
        ):
            args.append("-r")
        args.append("-e " + user_data["user_email"])
        args.append("-p " + password)
        try:
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
        except Exception as e:
            log.error(
                "CGIARADAuthenticationError: "
                "Error while excuting Java authenticating user {}. Error: {}".format(
                    user_data["user_email"], str(e)
                )
            )
            return False
        error_no = p.returncode
        if error_no == 0:
            return True
        else:
            if error_no == 1:
                log.error(
                    "CGIARADAuthenticationError: "
                    "Error while authenticating user {}. Error: {}-{}".format(
                        user_data["user_email"], stdout.decode(), stderr.decode()
                    )
                )
            if error_no == 2:
                log.error(
                    "CGIARADAuthenticationError: "
                    "User {} provided an invalid password".format(
                        user_data["user_email"]
                    )
                )
            return False

    def after_collaborator_login(self, request, collaborator):
        return True, ""
