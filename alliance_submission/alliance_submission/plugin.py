import formshare.plugins as plugins
import os
import shutil
from PIL import Image
import imghdr
from celerytasks import ftp_transfer


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
        if project == request.registry.settings.get("ftp.project"):
            settings = {}
            for key, value in request.registry.settings.items():
                if isinstance(value, str):
                    settings[key] = value
            # Call the Celery process to process any images into the FTP
            ftp_transfer.apply_async(
                (settings, submission,), queue="FormShare",
            )

    def after_processing_submission_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file
    ):
        pass

    # Implements IMedia
    def after_storing_media_in_repository(
        self, request, user, project, form, assistant, submission, json_file, media_file
    ):
        if project == request.registry.settings.get("ftp.project"):
            image = imghdr.what(media_file)
            if image is None:
                image = False
            else:
                image = True
            if image:
                ftp_repository_path = request.registry.settings.get(
                    "ftp.repository.path"
                )
                repository_path = os.path.join(ftp_repository_path, *[submission])
                os.makedirs(repository_path)

                file_name = submission + "_" + os.path.basename(media_file)
                repository_file = os.path.join(repository_path, *[file_name])
                # Copy the file into the repository
                shutil.copy(media_file, repository_file)
                # Reducing media file to 100X100 thumbnail
                im = Image.open(media_file)
                im.thumbnail((100, 100))
                im.save(media_file)

    def after_storing_media_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file, media_file
    ):
        pass
