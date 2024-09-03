import glob
from subprocess import Popen, PIPE
import os

ftp_server = "ftp.ciat.cgiar.org"
ftp_user = "artemis"
ftp_password = "4rt3m1-proj3c.24"
ftp_path = "/FOTOS"
form_id = "moment_3_vegetative"  # Change for each form
submission_array = ["00d1e1ff-303f-4e51-a5c6-6a1cbee817ba","00fc7f04-3a52-409c-940d-e211e526ccc9","02026786-23a3-4433-9ad9-a4e3eb513498","02104362-9fa9-4ace-be5e-d748643113b3","036d105d-485d-4316-9182-06b09efa10cf","05c9b41a-fff4-4cbc-a66b-51d35e308548","06b69dee-5e3b-413a-964a-a0be569855e9","08d87426-ff7b-48a9-aa23-29d3105f8079","0bf834c6-19bb-4702-88e8-3cd2f94819e7","0f48a4ac-16b1-40a6-a5df-b036b3cd8fa9","0fb68881-b3af-408d-94ed-ea70b1af9cbd","0ffa4ea7-0a52-4f7d-9dde-6c0f008211fa","0ffcf03c-52df-4afa-8dbd-0bc0efc14082","1065010e-6d67-4cd5-863c-33558efbe4e4","11bb9b1c-3480-4d9f-bfc9-ba2c76c5051b","1502ddf6-4874-48c2-b9f8-77a812def689","175cd231-5445-4c55-b69f-2fb2953e55ae","1885f6d1-5725-4ab8-9260-71df99632259","19bfb486-5a6b-4776-a5fa-b803c9d8f0b9","1a1e4190-9908-4e31-8f47-4fe333b1fb0f","1b6142e7-f9e8-40c0-b522-f1157fe518f5","1bba40c1-f181-4942-a1d1-4e45581dfea2","1c1154c3-b006-4a59-81bb-8974f8845b77","1c65671c-709b-4c0d-b3ad-f81cba230432","1d218662-fd91-4633-a0e4-21bd5683f7cb","1e9fcb31-44f4-4394-b7a7-9366e4a4e775","1ebe462c-d318-4c6c-bbb7-6ad532663b5d","1f758c0e-404e-44d7-aeb3-f2daa601ace0","20041fbe-71aa-4959-857b-0cc8c52f4c4d","201f2018-a0f8-4df5-8e14-08533da18803","2139361b-aa8d-4df2-a76e-a5b7caaf55ac","24d04ae0-3394-439f-a8a6-fdc0f515d3d1","265785b2-7a81-4ab4-9bb8-3243456c548b","274e8cd1-0324-47d0-9f6c-44839cba36aa","2bbdaaf1-6a0b-4236-8217-aa09f69110c3","2d9e0b31-ad30-4807-9211-598a2a09f9ba","30ad206b-4e57-424e-bba6-82250f818aae","3141d751-f830-425d-ae5c-b7b7b65b4095","40ce6c7d-43ed-46ec-a01e-af84b472c08e","4160e4d9-7cb3-42a5-a63a-037227b8f628","41c413d1-944a-47ff-ba79-bde9da98f8b5","435536f1-3c7c-431f-856b-33f73ecaae02","449294c0-348a-4d24-a8c0-c20d2b2696fb","4a16b1a9-45c9-485a-ac81-865f942c2d57","4a63ea37-b107-47df-adcf-cafbef11a7ca","4a82feaf-3bc6-4200-b973-29517cf784f3","4c08536e-a5e6-4dd0-9ce5-24a4bccb7f64","4c15538f-048e-42a9-87bf-8667eeacfda6","4c73ade6-8983-4eaf-b393-150f349969a7","504335e3-af0d-4f10-8fde-84d770ecb4b7","50518876-fff6-4dc8-bb54-41fb97ab3b52","50c1da8c-4dc9-44df-a1e8-d6106485bb37","50d9ac99-dd8c-460f-a5e5-5bd0051f44ac","521df625-8d55-4fb0-a031-e2344aa4edbf","52a2b85b-5f72-429c-8220-e785d5ca3d68","533e33dc-6588-4b4e-afcd-742bd49c8123","53966493-f4b8-491a-a720-097b65563451","54ddc84c-7c74-461a-9f8d-fb5dc772c216","55d7666a-dacd-4acc-8d5d-9252bbe05f68","57b45a28-5088-491b-ad17-b884171a28d0","5ab9417b-4989-47f8-8542-34078289b4ea","5c07438f-2ac5-4873-a574-30a0905abacc","5d76a11c-0cc8-4c60-9677-3b551b54fe17","5d845f1a-c261-4449-bcbf-3894fa33270c","5dbcd03f-6a8c-4a02-83bb-9f099ac864c6","5eb343a4-6a83-424b-9bb6-b4dcb7d34413","61b2793a-da0b-4d1c-8b3f-bf4ad68ef443","61eeefc4-dd5d-4a93-a183-ac137da33236","63b8b7ab-007a-4ec1-a504-b5ec9bbc7fc6","63c86006-d26e-4393-8c29-b0a3bfdeb3d8","65356cb5-0c49-444a-b32d-54f166229ba8","66f34a70-3032-4910-9252-2157484a16f0","68b2aa40-dae2-4d54-a16a-7b7bb08da44b","69681c22-061f-466b-b4e2-3cd627d9b5d3","6a7f4ea6-c1ca-44b2-b280-82946b550e50","6aac8c57-6c12-4955-9ce5-6c07aa22827d","6cb8fbdd-d5f7-48a8-9431-41ed79d7e0c7","6dcec13f-6fdc-426f-af76-8869900e5990","6e36f1a7-8577-4ca4-a264-e1e6901b1d68","6f0eaacd-a68a-48be-ab3d-70513072a458","70198d08-33c9-4415-b85a-0171b9bdb821","7062dd35-5cf5-4fa6-a530-f5f7e6cafad4","713606ae-7986-43d2-9f4c-7f7036a145e4","73f1d368-2d63-41e2-97ec-68749a0565f9","750c9c8b-7ae4-4972-a284-a1a63487b286","753e0d34-c0a4-4e14-b08e-62392420eeee","790e754f-97ab-406c-8b0b-73a996c64cc4","79840aea-6d8b-4be1-b44d-cdfd933a4209","7a4f9272-3ce0-4ca9-994a-d0551d9095ea","7ad6eac8-f3a2-477f-960b-d8361c564630","7fb44622-cf9e-456c-a255-b8e91b1997fd","8093f13c-4cb8-40bc-9d27-ecc8ae802e60","818a6fb3-16bf-4be3-a40d-5eaa8aad1611","823f70ef-b9ab-4d96-b060-fe8e30595930","82486127-f244-46fe-8c45-84d9f24067d5","83040e51-0435-46c8-b4c7-e2767adecacf","872b2883-b04b-4c54-a12a-f2a46ec1caf7","8abf5ecd-70ac-4cfb-81e8-2804db825c87","8b581b9a-9b02-44e2-9d49-11cafd2bdea8","8bbe589f-491c-4af2-b29f-2b54e5b09946","8ec50587-f1b3-476d-b1d6-123e3fa1e9af","8f08226c-80f2-4aaf-8ebb-447b8a740719","92f9db06-1f08-4cd7-8aeb-f8564234e439","968c0b7c-2692-4494-8b14-b36f6ef5ef4c","97e720c4-b796-4d4d-949b-7d6b6c42c0bf","9d8ef41f-9fc7-405d-82da-0e70e175cef4","9f565709-4ed9-4a6e-82c5-072406850812","9f6a8be3-1895-417b-8e59-572d265b3157","9f7ab213-341e-4ce5-aaf7-e00bc8b20252","a11bfe95-ceb5-4815-9339-47eee2d1b317","a50bb197-0921-4661-962e-2f0cf7b022de","a59da22c-677a-49b2-848f-8353612416e1","a5ebdd8c-b9e4-4fa8-ad17-3833805b79c8","a691c66c-736b-41e4-99ea-03eae8af5813","a6f39883-5e18-41a1-a1a5-c5d53dec9c5e","a7ff04a3-7859-4340-b0f0-2e6b0469b4dc","a85af22b-fac6-4b23-b168-69cac752cb71","abbe0f2d-df27-4bdc-98ee-404d2b00666b","ae967c23-784a-4ba7-8172-69f19eb03225","af1761e9-4713-4819-bf8a-10eb6f87258d","af6354f6-2b72-4d25-b38b-d81ffb4c0e60","af6ad00e-63fc-413d-83e6-dbed334a7148","b3a64d3e-2e9f-4f7c-a56b-0acbf88ef8a6","b6293e55-4c95-428b-95ab-259ef0a945d7","b6b632cd-f125-4843-a5df-28aeb3c5581a","b6b890ea-a9db-486e-a8bf-84ea6ab000b5","b70983b5-d554-4690-aefe-f67de8058b08","b8da1de0-ba4e-4d1c-8043-21ca84658103","b937885e-de2e-42a3-a057-7cff6d3a55ba","bbef3692-f617-4324-9848-612f9dde17c4","bbf03d42-c829-4877-ba9a-a23d4cf64dac","bd005b48-cc43-4100-a925-59f53cdddf65","c04f18a0-4913-4923-8761-b02695db88a6","c1624804-b3b6-4a10-b71b-175ce1f38811","c3596ea9-e168-4e4e-869b-6b0ea311e7fa","c894e022-ff07-4157-aa4f-d25fad252473","ca800e3e-9730-45d3-824f-9d7a711278c6","cf6e61fe-0c9c-423f-8e6c-7f4e8094493e","d0a3ec30-ed8b-4a5e-8562-dc93da06ed2d","d49f4239-8808-4ccd-b8b4-7aeb58b8b4c4","d531b536-a0f3-4661-93fb-959d11982c59","d5797c45-b2ce-4c2d-9836-171995789980","dc2c06d8-9f1d-4fb0-af1a-95f6076c1641","dd9aabed-e0d2-4790-8fa6-88a92bf42c47","e1c5fae0-8c7c-474b-979f-30ecac328bd1","e23281d8-f239-48d1-99c9-bb8108ad4b37","e518737f-9df3-44b4-b0ac-46a4fe736d3a","e60aba22-4c4c-4261-b049-052d44dd830d","e9c7c7bb-fb2f-456e-ad65-e60813ba84b9","eaa7cf2b-7b8c-4d31-84e8-7affe920f7fb","eed0ff1f-9b23-49ab-a47f-15405c370161","eefba714-f1aa-40a8-ad55-0e21693fb325","ef860715-99d6-40be-bdbf-d546e94311b9","efe7202f-7207-48f7-b80f-6b5e5604182a","f3114234-0dce-4e61-9212-9f203604ff05","f4da82aa-9b33-4d2d-8eb6-24772902a9aa","f9244243-f21b-4a56-a465-3b4648051679","fb9713d6-458b-4c13-bb18-79d362999271","fd19f673-e29f-4d1d-ad6c-cff94403858d","fdb43fda-4ed2-43ee-bf38-1b04ee438a8b","fdff9aef-0e04-4de8-a1a4-80493ee7b6f0"]
send = False
directories = glob.glob("./*/")
for a_directory in directories:
    m4a = glob.glob(a_directory + "*.m4a")
    amr = glob.glob(a_directory + "*.amr")
    aac = glob.glob(a_directory + "*.aac")
    sounds = m4a + amr + aac
    submission = os.path.basename(os.path.normpath(a_directory))
    if submission in submission_array:
        for a_sound in sounds:
            # print("Submission: {}".format(submission))
            media_file = os.path.abspath(a_sound)
            file_name = os.path.basename(media_file)
            file_stats = os.stat(media_file)
            file_size = file_stats.st_size
            if file_size > 10:
                try:
                    if send:
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
                            "ftp://{}{}/{}_{}_{}".format(
                                ftp_server, ftp_path, form_id, submission, file_name
                            ),
                        ]
                        p = Popen(args, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = p.communicate()
                        if p.returncode == 0:
                            os.remove(media_file)
                            with open(media_file, "w") as file:
                                file.write("Moved to the FTP server")
                        else:
                            print(
                                "FTPStorageError: Sending file {}. Error: {}-{}".format(
                                    media_file, stdout.decode(), stderr.decode()
                                )
                            )
                    else:
                        print(
                            "Will move {} to {}".format(
                                media_file,
                                "ftp://{}{}/{}_{}_{}".format(
                                    ftp_server, ftp_path, form_id, submission, file_name
                                ),
                            )
                        )
                except Exception as e:
                    print(
                        "FTPStorageError: Cannot store file {} in FTP server for submission {}. "
                        "Error: {}".format(media_file, submission, str(e))
                    )
