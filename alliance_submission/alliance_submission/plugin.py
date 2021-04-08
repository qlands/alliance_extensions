import formshare.plugins as plugins
import ftplib
import os
import shutil
from PIL import Image
import imghdr


class AllianceSubmission(plugins.SingletonPlugin):
    plugins.implements(plugins.IMediaSubmission)

    def before_storing_media(
            self, request, user, project, form, assistant, submission, xml_file, media_file
    ):
        if project == request.registry.settings.get("ftp.project"):
            image = imghdr.what(media_file)
            if image is None:
                image = False
            else:
                image = True
            if image:
                ftp_server = request.registry.settings.get("ftp.server")
                ftp_user = request.registry.settings.get("ftp.user")
                ftp_password = request.registry.settings.get("ftp.password")
                ftp_path = request.registry.settings.get("ftp.path")
                try:
                    session = ftplib.FTP(ftp_server, ftp_user, ftp_password)
                    file_name = submission + "_" + os.path.basename(media_file)
                    file = open(media_file, 'rb')
                    ftp_file = os.path.join(ftp_path, *[file_name])
                    session.storbinary('STOR {}'.format(ftp_file), file)
                    file.close()  # close file and FTP
                    session.quit()
                except Exception as e:
                    print("FTPStorageError: Cannot store file {} in FTP server. Error: {}".format(media_file, str(e)))
                    ftp_fallback_path = request.registry.settings.get("ftp.fallback.path")
                    file_name = submission + "_" + os.path.basename(media_file)
                    fallback_file = os.path.join(ftp_fallback_path, *[file_name])
                    shutil.copy(media_file, fallback_file)
                # Reducing media file to 100X100 thumbnail
                im = Image.open(media_file)
                im.thumbnail((100, 100))
                im.save(media_file)
        return True

    def after_storing_media(
            self, request, user, project, form, assistant, submission, xml_file, media_file
    ):
        pass
