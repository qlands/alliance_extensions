import glob
from subprocess import Popen, PIPE
import os
import re

ftp_server = "ftp.ciat.cgiar.org"
ftp_user = "artemis"
ftp_password = "4rt3m1-proj3c.24"

send = False
directories = glob.glob("./*/")
for a_directory in directories:
    m4a = glob.glob(a_directory + "*.m4a")
    amr = glob.glob(a_directory + "*.amr")
    aac = glob.glob(a_directory + "*.aac")
    jpg = glob.glob(a_directory + "*.jpg")
    media_files = m4a + amr + aac + jpg
    for a_file in media_files:
        file_name = os.path.basename(a_file)

        matches = re.finditer(r"_", file_name)
        positions = [match.start() for match in matches]
        last_two_positions = positions[-2:]

        # Split the string at the last two underscores
        media_file_name = file_name[last_two_positions[1] + 1:]
        submission_id = file_name[
                          last_two_positions[0] + 1: last_two_positions[1]
                          ]
        form_id = file_name[: last_two_positions[0]]
        ftp_path = "/FOTOS"

        if form_id == "plant_level_ground_truth":
            ftp_path = "/plant_level_ground_truth"

        if form_id == "arusha_cb_metricstrial_subversion":
            ftp_path = "/arusha_cb_metricstrial_subversion"

        if form_id == "ps_emergence_subversion":
            ftp_path = "/ps_emergence_subversion"

        if form_id == "ps_emergence":
            ftp_path = "/ps_emergence"

        if form_id == "arusha_cb_metricstrial_alta":
            ftp_path = "/arusha_cb_metricstrial_alta"

        if form_id == "50_percent_flowering":
            ftp_path = "/50_percent_flowering"

        if form_id == "arusha_cb_metricstrial":
            ftp_path = "/arusha_cb_metricstrial"

        if form_id == "sop_dev_colombia_cb":
            ftp_path = "/sop_dev_colombia_cb"

        if ftp_path == "/FOTOS":
            target = "ftp://{}{}/{}_{}_{}".format(
                ftp_server, ftp_path, form_id, submission_id, file_name
            )
        else:
            target = "ftp://{}{}/{}/{}".format(
                ftp_server, ftp_path, submission_id, file_name
            )

        file_stats = os.stat(a_file)
        if file_name.upper().find("JPG") >= 0:
            file_size = file_stats.st_size / (1024 * 1024)
            file_min = 1
        else:
            file_size = file_stats.st_size
            file_min = 30
        if file_size > file_min:
            if send:
                args = [
                    "curl",
                    "--user",
                    "{}:{}".format(ftp_user, ftp_password),
                    "--ftp-create-dirs",
                    "--upload-file",
                    a_file,
                    target,
                ]
                p = Popen(args, stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                if p.returncode == 0:
                    os.remove(a_file)
                else:
                    print(
                        "FTPStorageError: Sending file {}. Error: {}-{}".format(
                            a_file, stdout.decode(), stderr.decode()
                        )
                    )
            else:
                print(
                    "Will move {} to {}".format(
                        a_file,
                        target,
                    )
                )