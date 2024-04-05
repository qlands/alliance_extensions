from formshare.config.celery_app import celeryApp
from formshare.config.celery_class import CeleryTask
import os
import glob
from subprocess import Popen, PIPE
import uuid
import datetime
import redis
from celery.utils.log import get_task_logger
from sqlalchemy import create_engine

log = get_task_logger(__name__)


@celeryApp.task(bind=True, base=CeleryTask)
def ftp_transfer(self, settings, submission):
    ftp_repository_path = settings.get("ftp.repository.path")
    repository_path = os.path.join(ftp_repository_path, *[submission])
    ftp_submission_db = settings.get("ftp.submission.db")
    if os.path.exists(repository_path):
        sqlite_engine = "sqlite:///{}".format(ftp_submission_db)
        create_table = False
        if not os.path.exists(ftp_submission_db):
            create_table = True
        engine = create_engine(sqlite_engine)
        if create_table:
            engine.execute(
                "CREATE TABLE IF NOT EXISTS submission (submission_id varchar(64),"
                "submission_datetime datetime,odk_submission varchar(64),submission_file TEXT,"
                "submission_size NUMERIC,submission_status INTEGER,PRIMARY KEY(submission_id))"
            )
        media_path = os.path.join(repository_path, *["*.*"])
        files = glob.glob(media_path)
        redis_host = settings.get("redis.sessions.host", "localhost")
        redis_port = int(settings.get("redis.sessions.port", "6379"))
        r = redis.Redis(host=redis_host, port=redis_port)

        for media_file in files:
            if self.is_aborted():
                return
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
                        args = [
                            "curl",
                            "--user",
                            "{}:{}".format(ftp_user, ftp_password),
                            "--upload-file",
                            media_file,
                            "ftp://{}{}".format(ftp_server, ftp_path),
                        ]
                        p = Popen(args, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = p.communicate()
                        if p.returncode != 0:
                            log.error(
                                "FTPStorageError: Sending file {}. Error: {}-{}".format(
                                    media_file, stdout.decode(), stderr.decode()
                                )
                            )
                            engine.execute(
                                "INSERT INTO submission (submission_id,submission_datetime,"
                                "odk_submission,submission_file,submission_size,submission_status) "
                                "VALUES ('{}','{}','{}','{}',{},{})".format(
                                    ftp_submission_id,
                                    datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    submission,
                                    media_file,
                                    os.path.getsize(media_file),
                                    1,
                                )
                            )
                        else:
                            ftp_submission_id = str(uuid.uuid4())
                            # noinspection SqlDialectInspection
                            engine.execute(
                                "INSERT INTO submission (submission_id,submission_datetime,"
                                "odk_submission,submission_file,submission_size,submission_status) "
                                "VALUES ('{}','{}','{}','{}',{},{})".format(
                                    ftp_submission_id,
                                    datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    submission,
                                    media_file,
                                    os.path.getsize(media_file),
                                    0,
                                )
                            )
                            try:
                                os.remove(media_file)
                            except Exception as e:
                                log.error(
                                    "Cannot remove file {}. Error: {}".format(
                                        media_file, str(e)
                                    )
                                )
                            print("File {} sent".format(media_file))
                    except Exception as e:
                        log.error(
                            "FTPStorageError: Cannot store file {} in FTP server for submission {}. "
                            "Error: {}".format(media_file, submission, str(e))
                        )
        engine.dispose()
