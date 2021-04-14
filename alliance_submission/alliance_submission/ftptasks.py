from formshare.config.celery_app import celeryApp
from formshare.config.celery_class import CeleryTask
import os
import glob
from subprocess import Popen, PIPE
import shutil
import redis
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@celeryApp.task(base=CeleryTask)
def ftp_transfer(settings, submission):
    ftp_repository_path = settings.get("ftp.repository.path")
    repository_path = os.path.join(ftp_repository_path, *[submission])
    if os.path.exists(repository_path):
        media_path = os.path.join(repository_path, *["*.*"])
        files = glob.glob(media_path)
        error = False

        redis_host = settings.get("redis.sessions.host", "localhost")
        redis_port = int(settings.get("redis.sessions.port", "6379"))
        r = redis.Redis(host=redis_host, port=redis_port)

        for media_file in files:
            if os.path.exists(media_file):
                redis_key = "ftp-{}".format(os.path.basename(media_file))
                if r.get(redis_key) is None:
                    r.mset({redis_key: 1})
                    ftp_server = settings.get("ftp.server")
                    ftp_user = settings.get("ftp.user")
                    ftp_password = settings.get("ftp.password")
                    ftp_path = settings.get("ftp.path")
                    try:
                        print("Sending file {}".format(media_file))
                        args = ["curl", "--user", "{}:{}".format(ftp_user, ftp_password),
                                "--upload-file", media_file, "ftp://{}{}".format(ftp_server, ftp_path)]
                        p = Popen(args, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = p.communicate()
                        if p.returncode != 0:
                            log.error("Error: {}-{}".format(stdout.decode(), stderr.decode()))
                        else:
                            try:
                                os.remove(media_file)
                            except Exception as e:
                                log.error("Cannot remove file {}. Error: {}".format(media_file, str(e)))
                            print("File {} sent".format(media_file))
                    except Exception as e:
                        log.error(
                            "FTPStorageError: Cannot store file {} in FTP server for submission {}. "
                            "Error: {}".format(media_file, submission, str(e))
                        )
