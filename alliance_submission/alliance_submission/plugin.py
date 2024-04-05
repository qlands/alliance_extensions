import formshare.plugins as plugins
import os
import shutil
from PIL import Image
import imghdr
import json
from alliance_submission.ftptasks import ftp_transfer


class AllianceSubmission(plugins.SingletonPlugin):
    plugins.implements(plugins.IMediaSubmission)
    plugins.implements(plugins.IJSONSubmission)

    # Implements IJSONSubmission
    def before_processing_submission(
        self, request, user, project, form, assistant, json_file
    ):
        return 0, ""

    def after_processing_submission_in_repository(
        self, request, user, project, form, assistant, submission, error, json_file
    ):
        settings_file = request.registry.settings.get("ftp.settings.file")
        f = open(settings_file)
        ftp_settings = json.load(f)
        f.close()
        for a_setting in ftp_settings:
            forms = a_setting.get("ftp.forms", "")
            forms = forms.split(",")
            if forms[0] == "":
                forms = []
            if project == a_setting.get("ftp.project") and (
                form in forms or len(forms) == 0
            ):
                # Call the Celery process to process any images into the FTP
                ftp_transfer.apply_async(
                    (
                        a_setting,
                        submission,
                    ),
                    queue="FormShare",
                )

    def after_processing_submission_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file
    ):
        pass

    # Implements IMedia
    def after_storing_media_in_repository(
        self, request, user, project, form, assistant, submission, json_file, media_file
    ):
        settings_file = request.registry.settings.get("ftp.settings.file")
        f = open(settings_file)
        ftp_settings = json.load(f)
        f.close()
        for a_setting in ftp_settings:
            forms = a_setting.get("ftp.forms", "")
            forms = forms.split(",")
            if forms[0] == "":
                forms = []
            if project == a_setting.get("ftp.project") and (
                form in forms or len(forms) == 0
            ):
                image = imghdr.what(media_file)
                if image is None:
                    image = False
                else:
                    image = True
                if image:
                    ftp_repository_path = a_setting.get("ftp.repository.path")
                    repository_path = os.path.join(ftp_repository_path, *[submission])
                    if not os.path.exists(repository_path):
                        os.makedirs(repository_path)

                    file_name = (
                        form + "_" + submission + "_" + os.path.basename(media_file)
                    )
                    repository_file = os.path.join(repository_path, *[file_name])
                    # Copy the file into the repository
                    shutil.copy(media_file, repository_file)
                    # Reducing media file to 100X100 thumbnail
                    im = Image.open(media_file)
                    im.thumbnail((100, 100))
                    im.save(media_file)
                else:
                    if (
                        os.path.basename(media_file).upper().index(".M4A") >= 0
                        or os.path.basename(media_file).upper().index(".AMR") >= 0
                    ):
                        ftp_repository_path = a_setting.get("ftp.repository.path")
                        repository_path = os.path.join(
                            ftp_repository_path, *[submission]
                        )
                        if not os.path.exists(repository_path):
                            os.makedirs(repository_path)

                        file_name = (
                            form + "_" + submission + "_" + os.path.basename(media_file)
                        )
                        repository_file = os.path.join(repository_path, *[file_name])
                        shutil.copy(media_file, repository_file)
                        # We leave a file here just as a placeholder
                        os.remove(media_file)
                        with open(media_file, "w") as file:
                            file.write("Moved to the FTP server")

    def after_storing_media_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file, media_file
    ):
        pass
