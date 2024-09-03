import glob
from PIL import Image
from subprocess import Popen, PIPE
import os

ftp_server = "ftp.ciat.cgiar.org"
ftp_user = "artemis"
ftp_password = "4rt3m1-proj3c.24"
ftp_path = "/plant_level_ground_truth"

submission_array = [
    "0ff4ab27-e3e0-410c-8cc5-5ce5ab379a1c",
    "14e81c76-5ee7-4995-93d4-b7adf2a74ca5",
    "19ea75d0-a9d8-4570-8b84-89635a1786e5",
    "1bc91a07-7a7c-4d50-b8e3-db910de9cc1c",
    "38b56a60-ddd9-425a-833b-00744a1504e1",
    "4293fd8b-9ed5-4798-ab74-1e0aa2d4fb6c",
    "4e34f6bc-1ee3-471c-b174-abc08e7283a0",
    "5236d01d-897a-4c90-a21b-5a3581bcb192",
    "572c4380-1ba6-4f10-97d9-5d38280bc5a2",
    "5d085547-7438-4ca3-a1dd-7203d6d6f2a6",
    "6ec1776e-19ce-4907-b010-7b8ee32ff833",
    "6f1d10c9-ada4-4c87-a9a5-de1ec8fcae8d",
    "7ae8916b-7ac7-482a-8929-eff87b0e7f3e",
    "824882f0-8c38-444c-b0ed-470fa4c4ac04",
    "858aecd2-1885-4791-95df-333ee767be27",
    "8afcb409-abc5-42be-9d05-fb3a312ec169",
    "94e30cad-0847-4b33-8715-c1af37407b1e",
    "9905a8c8-e3af-4c59-b6fe-25439ce0b016",
    "99ceabcb-19d0-441f-b890-60f4ae3e6198",
    "a40672fa-8d49-4b7c-ba4b-7f6155c2471e",
    "a5c1a932-d5bd-45ce-8f45-2cb2dfb618a7",
    "aa68cef1-1ad4-42c7-97dd-c543d30b24eb",
    "b2e333e8-ac80-4224-b039-b29fda845988",
    "b49743a2-1659-4e80-9d3d-3fbf8b782d17",
    "bee45032-feda-4341-976b-1b074823baf8",
    "c4fc217e-96c1-47e6-8f4a-6ab721e0ae5b",
    "de86e131-172d-47e2-9eca-41042f7d49d7",
    "e9ba9d02-a7d8-4300-a003-724761b8e2e7",
    "ef9ecfda-aaad-4120-a5ea-2b58817e6f40",
    "f11aaddd-7200-4461-b741-009cd570b7cb",
    "f439abd9-0e98-4d4c-8906-d5908e4d3b5e",
]

directories = glob.glob("./*/")
for a_directory in directories:
    images = glob.glob(a_directory + "*.jpg")
    submission = os.path.basename(os.path.normpath(a_directory))
    if submission in submission_array:
        for an_image in images:
            # print("Submission: {}".format(submission))
            media_file = os.path.abspath(an_image)
            file_name = os.path.basename(media_file)
            file_stats = os.stat(media_file)
            file_size = file_stats.st_size / (1024 * 1024)
            if file_size > 1:
                try:
                    send_to = "ftp://{}{}/{}/{}".format(
                        ftp_server, ftp_path, submission, file_name
                    )
                    print(
                        "Sending file {}, {} to: {}".format(
                            media_file, file_name, send_to
                        )
                    )
                    args = [
                        "curl",
                        "--user",
                        "{}:{}".format(ftp_user, ftp_password),
                        "--ftp-create-dirs",
                        "--upload-file",
                        media_file,
                        "ftp://{}{}/{}/{}".format(
                            ftp_server, ftp_path, submission, file_name
                        ),
                    ]
                    p = Popen(args, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = p.communicate()
                    if p.returncode == 0:
                        im = Image.open(media_file)
                        im.thumbnail((100, 100))
                        im.save(media_file)
                    else:
                        print(
                            "FTPStorageError: Sending file {}. Error: {}-{}".format(
                                media_file, stdout.decode(), stderr.decode()
                            )
                        )
                except Exception as e:
                    print(
                        "FTPStorageError: Cannot store file {} in FTP server for submission {}. "
                        "Error: {}".format(media_file, submission, str(e))
                    )
