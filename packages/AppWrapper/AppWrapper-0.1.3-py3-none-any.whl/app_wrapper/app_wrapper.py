import ast
import json
import os
import pathlib
import traceback
from enum import Enum

import requests


class Status(str, Enum):
    Complete = "Complete"
    Processing = "Processing"
    Failed = "Failed"
    Canceled = "Canceled"
    Scheduled = "Scheduled"
    Paused = "Paused"


class AppWrapper:
    def __init__(self):
        try:
            self.TOAD_HOST = os.getenv("TOAD_HOST", None)
            self.task_id = os.environ["TASK_ID"]
            self.main_app_id = os.environ["MAIN_APP_ID"]
            self.file_folder = os.environ["POD_FILE_PATH"]
            self.app_input_files = ast.literal_eval(
                os.environ["APP_INPUT_FILES"]
            )

            if len(self.app_input_files) != 0:
                self.download_file_from_s3()
        except Exception as e:
            error_log = f"Initialization Failed: {str(e)}"
            self.update_status(Status.Failed.value, error_log)

    def download_file_from_s3(self):
        for index, s3_path in enumerate(self.app_input_files):
            file_key = s3_path.split("/")[2]

            presigned_get_url = requests.get(
                f"{self.TOAD_HOST}/utils/presigned-download-url/?app_id={self.main_app_id}&task_id={self.task_id}&file_name={file_key}"
            ).json()["url"]

            res = requests.get(presigned_get_url)

            if res.status_code != 200:
                error_log = f"Failed: File download. \
                                    status code: {res.status_code} detail: {res.reason} \
                                    file_key: {file_key} presigned url: {presigned_get_url}"
                self.update_status(Status.Failed.value, error_log)

            file_path = os.path.join(self.file_folder, file_key)
            pathlib.Path(file_path).parents[0].mkdir(
                parents=True, exist_ok=True
            )
            with open(file_path, "wb") as f:
                f.write(res.content)

    def upload_file_to_s3(self, result):
        file_path = result["file_path"]
        file_name = file_path.split("/")[-1]

        presigned_put_url = requests.get(
            f"{self.TOAD_HOST}/utils/presigned-upload-url/?app_id={self.main_app_id}&task_id={self.task_id}&file_name={file_name}"
        ).json()["url"]

        with open(file_path, "rb") as file:
            res = requests.put(presigned_put_url, data=file)

        if res.status_code != 200:
            error_log = f"Failed: File upload. \
                            status code: {res.status_code} detail: {res.reason} \
                            file_key: {file_name} presigned url: {presigned_put_url}"
            self.update_status(Status.Failed.value, error_log)

    def update_status(self, status: Status, log: str):
        print(f"[AppWrapper] - {log}")
        requests.put(
            f"{self.TOAD_HOST}/tasks/{self.task_id}/status/{status}/log/",
            data=json.dumps({"log": f"[AppWrapper] - {log}"}),
        )
        if status == "Failed":
            exit()

    def validate_result_format(self, result: dict):
        if not isinstance(result, dict) or "type" not in result:
            error_log = "App result should include 'type' key"
            self.update_status(Status.Failed.value, error_log)

        if result["type"] == "link" and "url" not in result:
            error_log = "App result should include 'url' key for link type"
            self.update_status(Status.Failed.value, error_log)

        if result["type"] == "download" and "file_path" not in result:
            error_log = (
                "App result should include 'file_path' key for download type"
            )
            self.update_status(Status.Failed.value, error_log)

    def __call__(self, func):
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                print(traceback.print_exc())
                error_log = f"App failed: {e}"
                self.update_status(Status.Failed.value, error_log)

            try:
                self.validate_result_format(result)

                if result["type"] == "download":
                    self.upload_file_to_s3(result)

                data = {"task_id": self.task_id, "result": result}

                requests.post(
                    f"{self.TOAD_HOST}/output/", data=json.dumps(data)
                )

                self.update_status(Status.Complete.value, log="Job completed")

            except Exception as e:
                error_log = f"Post app failed: {e}"
                self.update_status(Status.Failed.value, error_log)

        return inner
