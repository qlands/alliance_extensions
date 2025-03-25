import formshare.plugins as plugins
from formshare.processes.db.form import get_form_data
from formshare.processes.odk.api import get_odk_path
from formshare.processes.email.send_email import send_email
import os
import glob
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import logging
import time


log = logging.getLogger("formshare")


def get_data(request, sql, just_one=True):
    sql_url = request.registry.settings.get("sqlalchemy.url")
    engine = create_engine(sql_url, poolclass=NullPool)
    try:
        connection = engine.connect()
        if just_one:
            data = connection.execute(sql).fetchone()
        else:
            data = connection.execute(sql).fetchall()
        connection.invalidate()
        engine.dispose()
        return data

    except Exception as e:
        log.error("MediaCheck - Error connecting to MySQL: {} ".format(str(e)))


class AllianceMediaCheck(plugins.SingletonPlugin):
    plugins.implements(plugins.IJSONSubmission)

    # Implements IJSONSubmission
    def before_processing_submission(
        self, request, user, project, form, assistant, json_file
    ):
        return 0, ""

    def after_processing_submission_in_repository(
        self, request, user, project, form, assistant, submission, error, json_file
    ):
        form_schema = "FS_fb615be7_f320_49cd_801e_24bf7047b97b"
        project_id = "39f30325-5eaf-404e-97b1-9857cd00e287"
        email_to = "alliance-dm@cgiar.org"

        # -----------Testing
        # form_schema = "FS_acfeadf3_030f_41c1_946c_4d97e88af848"
        # project_id = "06fc3e7b-45a4-45b4-b159-d4a6306705b4"
        # email_to = "cquiros@qlands.com"
        # time.sleep(30)
        # -------------------
        form_id = "Reporte_eventos"

        if project == project_id and form.find(form_id) >= 0:
            media_files = []
            form_data = get_form_data(request, project, form)

            sql = (
                "SELECT id_unique,b21,e30,b22 FROM {}.maintable "
                "WHERE surveyid = '{}'"
            ).format(form_schema, submission)

            main_info = get_data(request, sql)
            if main_info is not None:
                primary_key = main_info[0]
                if main_info[1] is not None:
                    media_files.append(main_info[1])
                if main_info[2] is not None:
                    media_files.append(main_info[2])
                if main_info[3] is not None:
                    media_files.append(main_info[3])
            else:
                log.error(
                    "MediaCheck - Submission {} is not in database".format(submission)
                )
                return

            sql = "SELECT b24 FROM {}.b24_ WHERE id_unique = '{}'".format(
                form_schema, primary_key
            )
            images = get_data(request, sql, False)
            if images is not None:
                for an_image in images:
                    media_files.append(an_image[0])
            else:
                log.error(
                    "MediaCheck - Submission {} does not have images in the repeat".format(
                        submission
                    )
                )
            if media_files:
                try:
                    form_directory = form_data["form_directory"]
                    odk_directory = get_odk_path(request)
                    media_directory = os.path.join(
                        odk_directory,
                        *["forms", form_directory, "submissions", submission]
                    )
                    if os.path.exists(media_directory):
                        submitted_files = []
                        for a_file in glob.iglob(media_directory + "/*"):
                            submitted_files.append(os.path.basename(a_file))
                        not_found_media_files = []
                        for a_media_file in media_files:
                            found = False
                            if a_media_file in submitted_files:
                                found = True
                            if not found:
                                not_found_media_files.append(a_media_file)
                        if len(not_found_media_files) > 0:
                            not_found_string = ",".join(not_found_media_files)
                            message = "MediaCheck - Some media files are missing in submission {} ({}) by {}: {}".format(
                                submission, primary_key, assistant, not_found_string
                            )
                            log.error(message)
                            send_email(
                                request,
                                "no_reply@qlands.com",
                                email_to,
                                "Missing images in Reporte de Eventos",
                                message,
                            )
                            send_email(
                                request,
                                "no_reply@qlands.com",
                                "support_for_alliance@qlands.com",
                                "Missing images in Reporte de Eventos",
                                message,
                            )
                        else:
                            log.error(
                                "MediaCheck - No media files are missing in submission {}".format(
                                    submission
                                )
                            )
                    else:
                        log.error(
                            "MediaCheck - Submission {} has media files but not directory".format(
                                submission
                            )
                        )
                except Exception as e:
                    log.error(
                        "MediaCheck - Error checking submission: {}. {} ".format(
                            submission, str(e)
                        )
                    )
            else:
                log.error(
                    "MediaCheck - Submission {} does not have media files".format(
                        submission
                    )
                )

    def after_processing_submission_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file
    ):
        pass
