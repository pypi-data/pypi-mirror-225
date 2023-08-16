import json
import os
import ast
import requests
import pathlib


def wrapper():
    def decorator(func):
        def app_wrapper(*args, **kwargs):
            try:
                TOAD_HOST = os.getenv("TOAD_HOST", None)
                task_id = os.environ["TASK_ID"]
                main_app_id = os.environ["MAIN_APP_ID"]
                file_folder = os.environ["POD_FILE_PATH"]
                app_input_files = ast.literal_eval(
                    os.environ["APP_INPUT_FILES"]
                )

            except Exception as e:
                error_type = type(e).__name__
                error_log = (
                    f"[Pod] AppWrapper - Failed: {error_type} - {str(e)}"
                )
                print(f"[AppWrapper] {error_log}")
                requests.put(
                    f"{TOAD_HOST}/tasks/{task_id}/status/Failed/log/",
                    data=json.dumps({"log": f"AppWrapper - {error_log}"}),
                )
                exit()

            # input file이 있는 경우
            if len(app_input_files) != 0:
                for index, s3_path in enumerate(app_input_files):
                    file_key = s3_path.split("/")[2]

                    presigned_get_url = requests.get(
                        f"{TOAD_HOST}/utils/presigned-download-url/?app_id={main_app_id}&task_id={task_id}&file_name={file_key}"
                    ).json()["url"]

                    res = requests.get(presigned_get_url)

                    if res.status_code != 200:
                        error_log = f"[Pod] AppWrapper - Failed: File download. \
                                      status code: {res.status_code} detail: {res.reason} \
                                      file_key: {file_key} presigned url: {presigned_get_url}"
                        print(error_log)
                        requests.put(
                            f"{TOAD_HOST}/tasks/{task_id}/status/Failed/log/",
                            data=json.dumps(
                                {"log": f"AppWrapper - {error_log}"}
                            ),
                        )
                        exit()

                    file_path = os.path.join(file_folder, file_key)
                    pathlib.Path(file_path).parents[0].mkdir(
                        parents=True, exist_ok=True
                    )
                    with open(file_path, "wb") as f:
                        f.write(res.content)

            excluded_keys = ["email", "password"]
            excluded_values = [os.environ["ACCESS_KEY"]]

            print("[Input Infomation]")
            for key, value in kwargs.items():
                if key not in excluded_keys and value not in excluded_values:
                    print(f"{key}={value}")
            print("")

            try:
                result = func(*args, **kwargs)

            except Exception as e:
                print(e)
                requests.put(
                    f"{TOAD_HOST}/tasks/{task_id}/status/Failed/log/",
                    data=json.dumps({"log": f"Pod - Job failed: {e}"}),
                )
                exit()

            try:
                # result의 type
                result_type = result["type"]

                # app의 output에 파일있는 경우
                if result_type == "download":
                    file_path = result["file_path"]
                    file_name = file_path.split("/")[-1]

                    # file put하기 위한 url 요청
                    presigned_put_url = requests.get(
                        f"{TOAD_HOST}/utils/presigned-upload-url/?app_id={main_app_id}&task_id={task_id}&file_name={file_name}"
                    ).json()["url"]

                    with open(file_path, "rb") as file:
                        res = requests.put(presigned_put_url, data=file)

                    if res.status_code != 200:
                        error_log = f"[Pod] AppWrapper - Failed: File upload. \
                                      status code: {res.status_code} detail: {res.reason} \
                                      file_key: {file_key} presigned url: {presigned_put_url}"
                        print(error_log)

                        requests.put(
                            f"{TOAD_HOST}/tasks/{task_id}/status/Failed/log/",
                            data=json.dumps(
                                {"log": f"AppWrapper - {error_log}"}
                            ),
                        )
                        exit()

                # function의 result 전달
                data = {"task_id": task_id, "result": result}

                requests.post(f"{TOAD_HOST}/output/", data=json.dumps(data))

                requests.put(
                    f"{TOAD_HOST}/tasks/{task_id}/status/Complete/log/",
                    data=json.dumps({"log": "Pod - Job completed"}),
                )

            except Exception as e:
                error_log = f"AppWrapper - Post app failed: {e}"
                requests.put(
                    f"{TOAD_HOST}/tasks/{task_id}/status/Failed/log/",
                    data=json.dumps({"log": error_log}),
                )
                print(error_log)
                exit()

        return app_wrapper

    return decorator
