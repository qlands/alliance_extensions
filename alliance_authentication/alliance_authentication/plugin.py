import formshare.plugins as plugins
import formshare.plugins.utilities as u
import sys
import os
from subprocess import Popen, PIPE
import logging
from threading import Timer

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
        _ = request.translate
        java_java = request.registry.settings.get("java.authentication.jar")
        args = ["java", "-jar", java_java]
        if (
            request.registry.settings.get("java.authentication.remote", "false")
            == "true"
        ):
            args.append("-r")
        args.append("-e")
        args.append(user_data["user_email"])
        args.append("-p")
        args.append(password)
        time_out_flag = False

        def kill_time_out(process):
            nonlocal time_out_flag
            time_out_flag = True
            process.kill()

        try:
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            time_out = Timer(5, kill_time_out, [p])  # Wait 5 seconds to authenticate with CGIAR AD
            try:
                time_out.start()
                stdout, stderr = p.communicate()
            finally:
                time_out.cancel()
        except Exception as e:
            if not time_out_flag:
                log.error(
                    "CGIARADAuthenticationError: "
                    "Error while excuting Java authenticating user {}. Error: {}".format(
                        user_data["user_email"], str(e)
                    )
                )
                return False, _("Error while authenticating your account with the CGIAR AD")
            else:
                return False, _("Timeout while authenticating your account with the CGIAR AD")
        if time_out_flag:
            return False, _("Timeout while authenticating your account with the CGIAR AD")
        error_no = p.returncode
        if error_no == 0:
            return True, ""
        else:
            if error_no == 1:
                log.error(
                    "CGIARADAuthenticationError: "
                    "Error while authenticating user {}. Error: {}-{}".format(
                        user_data["user_email"], stdout.decode(), stderr.decode()
                    )
                )
                return False, _("Error while authenticating your account with the CGIAR AD")
            if error_no == 2:
                log.error(
                    "CGIARADAuthenticationError: "
                    "User {} provided an invalid password".format(
                        user_data["user_email"]
                    )
                )
                return False, _("The email account does not exist or the password is invalid")

    def after_collaborator_login(self, request, collaborator):
        return True, ""
