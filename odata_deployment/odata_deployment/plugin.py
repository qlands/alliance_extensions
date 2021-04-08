import formshare.plugins as plugins
from odata.plugins.interfaces import IWARFileCreated
from subprocess import Popen, PIPE
import logging

log = logging.getLogger("formshare")


class AllianceODataDeployment(plugins.SingletonPlugin):
    plugins.implements(IWARFileCreated)

    def after_create(self, request, absolute_path):
        _ = request.translate
        scp_cert_file = request.registry.settings.get("odata.scp.certfile")
        scp_cert_user = request.registry.settings.get("odata.scp.user")
        scp_cert_host = request.registry.settings.get("odata.scp.host")
        scp_cert_directory = request.registry.settings.get("odata.scp.directory")
        try:
            args = [
                "scp",
                "-i",
                scp_cert_file,
                absolute_path,
                "{}@{}:{}".format(scp_cert_user, scp_cert_host, scp_cert_directory),
            ]
            log.error("Deploying {} through SCP. Command: {}".format(absolute_path, " ".join(args)))
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            if p.returncode == 0:
                return True
            else:
                log.error(
                    "Error while deploying WAR file {} through SCP. Error: {}".format(
                        absolute_path, stdout.decode() + " " + stderr.decode()
                    )
                )
                return False
        except Exception as e:
            log.error(
                "Error while deploying WAR file {} through SCP. Error: {}".format(
                    absolute_path, str(e)
                )
            )
            return False