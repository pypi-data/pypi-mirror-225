import json
import logging
import os
import warnings
from http import HTTPStatus
from queue import LifoQueue
from time import sleep

import numpy as np
import requests

from .__consumer import Consumer
from .utils import AGGREGATED_OUTPUT_DIR, FILE_METADATA


class Client:
    def __init__(self,
                 credentials: dict,
                 host: str = "https://api.branchkey.com",
                 ssl: bool = True, 
                 wait_for_run: bool = False, 
                 run_check_interval_s: int = 30,
                 proxies : dict = None):

        if credentials is None:
            credentials = dict(leaf_name="guest", leaf_id="guest", leaf_session_token="guest",
                               response_host="response.branchkey.com", port=5672)
        self.__leaf_name = credentials["leaf_name"]
        self.__leaf_id = credentials["leaf_id"]
        self.__leaf_session_token = credentials["leaf_session_token"]
        self.__status = "unauthenticated"
        self.__tree_id = None
        self.__branch_id = None

        self.__api_host = host
        self.__proxies = proxies
        # Verify SSL certs
        self.__verify = ssl

        self.queue = LifoQueue(maxsize=1)
        self.__run_status = None
        self.__run_number = None
        self.__wait_for_run = wait_for_run
        self.__run_check_interval_s = run_check_interval_s

        self.rabbit_credentials = dict(
            leaf_name=self.__leaf_name, leaf_id=self.__leaf_id, queue_password=self.__leaf_session_token, host=credentials["response_host"])
        self.consumer = None

        self.__authenticate()
        self.get_run_details()
        return

    def __authenticate(self):
        try:
            url = self.__api_host + "/v1/leaf/authenticate"
            headers = {"accept": "application/json"}

            resp = requests.get(url, headers=headers,
                                auth=(self.__leaf_id, self.__leaf_session_token), verify=self.__verify, proxies=self.__proxies)

            print(f"received resp code form auth: {resp.status_code}")
            if resp.status_code != HTTPStatus.OK:
                raise Exception(resp.json())

            authenticate_data = resp.json()["data"]
            try:
                self.__status = "authenticated"
                self.__user_id = authenticate_data["user_id"]
                self.__tree_id = authenticate_data["tree_id"]
                self.__branch_id = authenticate_data["branch_id"]
                self.rabbit_credentials["tree_id"] = authenticate_data["tree_id"]
                self.rabbit_credentials["branch_id"] = authenticate_data["branch_id"]
                consumer = Consumer(self.rabbit_credentials,
                                    self.queue, self.__update_run_status)
                self.consumer = consumer.spawn_consumer_thread()
            except Exception as e:
                raise Exception(
                    f"Failed to parse response from authenticate API: {e}")

        except Exception as e:
            msg = "Authentication failed for leaf {}: {}".format(
                self.__leaf_name, e)
            raise Exception(msg)

    def get_run_details(self):
        try:
            url = self.__api_host + "/v1/branch/" + self.__branch_id + "/run"
            headers = {"accept": "application/json", "leaf": "true"}

            resp = requests.get(url, headers=headers,
                                auth=(self.__leaf_id, self.__leaf_session_token), verify=self.__verify, proxies=self.__proxies)

            print(
                f"received resp code from api-gateway for get_run_details: {resp.status_code}")
            if resp.status_code != HTTPStatus.OK:
                raise Exception(resp.json())

            run_details = resp.json()["data"]
            try:
                self.__run_status = run_details["run_status"]
                self.__run_number = run_details["run_number"]
            except Exception as e:
                raise Exception(
                    f"Failed to parse response from get_run_details API: {e}")

        except Exception as e:
            msg = "Getting Run details failed: {}".format(e)
            raise Exception(msg)

    def __update_run_status(self, status):
        self.__run_status = status
        if status == "start":
            self.get_run_details()

    def disable_ssl_verification(self, enabled=False):
        warnings.warn(
            "[BranchKey] We highly recommend enabling ssl verification. Use this at your own risk.")
        self.__verify = enabled
        return self.__verify

    def convert_pytorch_numpy(self, model, weighting=1):
        """
        Usage:
        update = convert_pytorch_numpy(model.get_params(), client_samples=5*5)
        :param model: Pytorch model parameters
        :param weighting: Weight given to this update. Usually the number of client samples used to construct the model
        :return: type(np.ndarray) of parameters
        """
        params = []
        for param in model:
            params.append(param[1].data.cpu().detach().numpy())
        numpy = (weighting, params)
        return np.asarray(numpy, dtype=object)

    def validate_weight_shape(self, file):
        """
        Validates that the weights are in the correct shape before being sent to the API
        :param file: file bytes or file path
        :return: True on success, otherwise returns an exception
        """
        array = np.load(file, allow_pickle=True)
        if array.shape[0] != 2:
            raise Exception("[validate_weight_shape] Incorrect shape != 2")
        elif type(array[0]) is not int:
            raise Exception("[validate_weight_shape] Dim 0 not integer")
        elif type(array[1]) is not list:
            raise Exception("[validate_weight_shape] Dim 1 not list")
        elif type(array[1][0]) is not np.ndarray:
            raise Exception("[validate_weight_shape] Dim 1:0 not ndarray")
        else:
            file.seek(0)
            return True

    def file_upload(self, file_path):
        try:
            if self.__run_status != "start":
                if self.__wait_for_run:
                    while self.__run_status != "start":
                        print(
                            f"run is blocked, going into sleep for {self.__run_check_interval_s} seconds before checking again")
                        sleep(self.__run_check_interval_s)
                else:
                    raise Exception("run is blocked")

            with open(file_path, mode="rb") as f:
                self.validate_weight_shape(f)

                url = self.__api_host + "/v1/file/upload"
                headers = {"accept": "application/json"}
                data = {"data": json.dumps({"leaf_name": self.__leaf_name,
                                            "metadata": FILE_METADATA})}
                file = {"file": f}

                resp = requests.post(
                    url, files=file, data=data, headers=headers,
                    auth=(self.__leaf_id, self.__leaf_session_token), verify=self.__verify, proxies=self.__proxies)
                f.close()

                if resp.status_code != HTTPStatus.CREATED:
                    raise Exception(resp.json()["error"])
                else:
                    return resp.json()["data"]["file_id"]

        except Exception as e:
            msg = "File Upload failed for leaf {} for file {}: {}".format(
                self.__leaf_name, file_path, e)
            raise Exception(msg)

    def file_download(self, file_id):
        try:
            if not os.path.exists(AGGREGATED_OUTPUT_DIR):
                os.makedirs(AGGREGATED_OUTPUT_DIR)

            url = self.__api_host + "/v1/file/download/" + file_id
            headers = {"accept": "*/*S"}
            resp = requests.get(url, headers=headers,
                                auth=(self.__leaf_id, self.__leaf_session_token), verify=self.__verify, proxies=self.__proxies)

            if resp.status_code != HTTPStatus.OK:
                raise Exception(resp.json()["error"])

            try:
                download_url = resp.json()["data"]["download_url"]
            except Exception as e:
                raise Exception(
                    f"Failed to parse response from download API: {resp.json()}")

            resp = requests.get(download_url, verify=self.__verify, proxies=self.__proxies)
            if len(resp.content) == 0:
                raise Exception("file not received")

            f = open(AGGREGATED_OUTPUT_DIR +
                     '/' + file_id + ".npy", 'wb')
            f.write(resp.content)
            f.close()
            print(f"downloaded file {file_id}")
            return True

        except Exception as e:
            msg = "File Download failed for leaf {} for file {}: {}".format(
                self.__leaf_name, file_id, e)
            raise Exception(msg)

    def send_performance_metrics(self, aggregation_id: str, data: str, mode: str):
        try:
            url = self.__api_host + "/v1/performance/analysis"
            headers = {"accept": "application/json"}
            data = json.dumps({"mode": mode,
                               "aggregation_id": aggregation_id,
                               "leaf_id": self.__leaf_id,
                               "branch_id": self.__branch_id,
                               "tree_id": self.__tree_id,
                               "data": data})

            resp = requests.post(url, headers=headers, data=data,
                                 auth=(self.__leaf_id, self.__leaf_session_token), verify=self.__verify, proxies=self.__proxies)

            print(
                f"received resp code form performance_analyser: {resp.status_code}")
            if resp.status_code != HTTPStatus.CREATED:
                raise Exception(resp.json())
            else:
                return True

        except Exception as e:
            msg = "Sending Performance Metrics failed for aggregation {}: {}".format(
                aggregation_id, e)
            logging.error(msg)
            return False

    @property
    def leaf_id(self):
        return self.__leaf_id

    @property
    def branch_id(self):
        return self.__branch_id

    @property
    def tree_id(self):
        return self.__tree_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def session_token(self):
        return self.__leaf_session_token

    @property
    def is_authenticated(self):
        return self.__status == "authenticated"

    @property
    def run_status(self):
        return self.__run_status

    @property
    def run_number(self):
        return self.__run_number
