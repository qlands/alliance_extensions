from formshare.config.celery_app import celeryApp
from formshare.config.celery_class import CeleryTask
import os
import glob
import ftplib
import shutil
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
        for media_file in files:
            ftp_server = settings.get("ftp.server")
            ftp_user = settings.get("ftp.user")
            ftp_password = settings.get("ftp.password")
            ftp_path = settings.get("ftp.path")
            try:
                session = ftplib.FTP(ftp_server, ftp_user, ftp_password)
                file_name = submission + "_" + os.path.basename(media_file)
                file = open(media_file, "rb")
                ftp_file = os.path.join(ftp_path, *[file_name])
                session.storbinary("STOR {}".format(ftp_file), file)
                file.close()  # close file and FTP
                session.quit()
                os.remove(media_file)
            except Exception as e:
                log.error(
                    "FTPStorageError: Cannot store file {} in FTP server for submission {}. "
                    "Error: {}".format(media_file, submission, str(e))
                )
                error = True
        if not error:
            try:
                shutil.rmtree(repository_path)
            except Exception as e:
                log.error(
                    "FTPStorageError: Cannot remove repository path {} for submission {}. "
                    "Error: {}".format(repository_path, submission, str(e))
                )
