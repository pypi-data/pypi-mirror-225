import logging
import os
from importlib import import_module
from time import sleep
from typing import Callable, List, Protocol, Dict, Any

from dynamofl.api.DatasourceAPI import DatasourceAPI
from dynamofl.Request import _Request

from .api.ProjectAPI import ProjectAPI
from .Datasource import _Datasource
from .Project import _Project
from .Helpers import TrainArgs, TestArgs

logger = logging.getLogger("State")

DEFAULT_TRAINER_NAME = "default"


class TrainFunction(Protocol):
    def __call__(self, args: TrainArgs) -> None:
        ...


class TestFunction(Protocol):
    def __call__(self, args: TestArgs) -> None:
        ...


class _State:
    """
    Error callbacks are called when an error occurs in the state.
    If a federation fails to complete or if a connection is lost, the error callback is called.
    """

    error_callbacks: List[Callable[[str], None]] = []
    test_method_callbacks: List[TestFunction] = []
    train_method_callbacks: List[TrainFunction] = []

    def __init__(self, token, host="https://api.dynamofl.com", metadata=None):
        self.token = token
        self.host = host

        self.datasources: dict[str, _Datasource] = {}
        self.instance_id = None
        self.metadata = metadata

        self.request = _Request(host=host, token=token)

        self.project_api = ProjectAPI(self.request)
        self.datasource_api = DatasourceAPI(self.request)

    def _get_last_fed_model_round(self, current_round, is_complete):
        if is_complete:
            return current_round
        else:
            return current_round - 1

    def _check_if_model_downloaded(self, federated_model_path):
        return os.path.exists(federated_model_path)

    def add_error_callback_for_testing(self, callback):
        self.error_callbacks.append(callback)

    def _add_test_method_callback(self, callback: TestFunction):
        self.test_method_callbacks.append(callback)

    def _add_train_method_callback(self, callback: TrainFunction):
        self.train_method_callbacks.append(callback)

    def test_callback(self, j, _):
        """
        Condition: yes_stats <- False
        """
        test_samples = (
            list(j["data"]["testSamples"].keys()) if "testSamples" in j["data"] else []
        )

        for datasource_key in test_samples:
            project_info = j["data"]["project"]
            trainer_key = j["data"]["testSamples"][datasource_key]["trainerKey"]

            project_key = project_info["key"]
            project = _Project(key=project_key, api=self.project_api)

            # on some project round completed
            # get appropriate train, test methods

            if datasource_key not in self.datasources or (
                trainer_key not in self.datasources[datasource_key].trainers
                and not project_info["hasDynamicTrainer"]
            ):
                continue

            if project_info["hasDynamicTrainer"]:
                mod = import_module(f"dynamic_trainers.{project_key}.train")
                test = getattr(mod, "test")
            else:
                test = self.datasources[datasource_key].trainers[trainer_key]["test"]
            model_path = "models"
            if "model_path" in self.datasources[datasource_key].trainers.get(
                trainer_key, {}
            ):
                model_path = self.datasources[datasource_key].trainers[trainer_key][
                    "model_path"
                ]

            model_extension = project_info["modelType"]
            current_round = project_info["currentRound"]
            prev_round = self._get_last_fed_model_round(
                current_round, project_info["isComplete"]
            )
            federated_model_path = get_federated_path(
                project_key, model_path, model_extension, datasource_key, prev_round
            )

            if not self._check_if_model_downloaded(federated_model_path):
                # Pull
                logger.info(
                    f"({project_key}-{datasource_key}) Waiting to download round ({prev_round}) federated model..."
                )
                project.pull_model(
                    federated_model_path,
                    round=prev_round,
                    datasource_key=datasource_key,
                    federated_model=True,
                )

            # Test
            logger.info(
                f"({project_key}-{datasource_key}) Running validation on round ({prev_round}) federated model..."
            )
            args = TestArgs(
                datasource_key=datasource_key,
                federated_model_path=federated_model_path,
                project_info=project_info,
            )

            test_res = test(args)
            for callback in self.test_method_callbacks:
                callback(args)
            if test_res is not None:
                scores, num_samples = test_res
                logger.info(scores)
                logger.info(f"({project_key}-{datasource_key}) Uploading scores...")
                project.report_stats(scores, num_samples, prev_round, datasource_key)
                logger.info("Done.")

    def train_callback(self, j, _):
        """
        Conditions: yes_submission <- False
        """
        train_samples = (
            list(j["data"]["trainSamples"].keys())
            if "trainSamples" in j["data"]
            else []
        )

        for datasource_key in train_samples:
            project_info = j["data"]["project"]
            trainer_key = j["data"]["trainSamples"][datasource_key]["trainerKey"]
            hyper_param_values = j["data"]["trainSamples"][datasource_key][
                "hyperParamValues"
            ]

            project_key = project_info["key"]
            project = _Project(key=project_key, api=self.project_api)

            # on some project round completed
            # get appropriate train, test methods

            if datasource_key not in self.datasources or (
                trainer_key not in self.datasources[datasource_key].trainers
                and not project_info["hasDynamicTrainer"]
            ):
                continue

            if project_info["hasDynamicTrainer"]:
                mod = import_module(f"dynamic_trainers.{project_key}.train")
                train = getattr(mod, "train")
            else:
                train = (
                    self.datasources[datasource_key].trainers[trainer_key].get("train")
                )
            model_path = "models"
            if "model_path" in self.datasources[datasource_key].trainers.get(
                trainer_key, {}
            ):
                model_path = self.datasources[datasource_key].trainers[trainer_key][
                    "model_path"
                ]

            model_extension = project_info["modelType"]
            current_round = project_info["currentRound"]
            prev_round = self._get_last_fed_model_round(
                current_round, project_info["isComplete"]
            )
            federated_model_path = get_federated_path(
                project_key, model_path, model_extension, datasource_key, prev_round
            )

            if not self._check_if_model_downloaded(federated_model_path):
                # Pull
                if not project_info["isCentralized"]:
                    logger.info(
                        f"({project_key}-{datasource_key}) Waiting to download round ({prev_round}) federated model..."
                    )

                    project.pull_model(
                        federated_model_path,
                        round=prev_round,
                        datasource_key=datasource_key,
                        federated_model=True,
                    )

            # Train and push
            new_model_path = get_trained_path(
                project_key, model_path, model_extension, datasource_key, current_round
            )

            logger.info(
                f"({project_key}-{datasource_key}) Training weights on local model..."
            )

            train_res = None
            if train:
                args = None
                if project_info["isCentralized"]:
                    args = TrainArgs(
                        datasource_key=datasource_key,
                        project_info=project_info,
                        hyper_param_values=hyper_param_values,
                    )
                else:
                    args = TrainArgs(
                        datasource_key=datasource_key,
                        federated_model_path=federated_model_path,
                        new_model_path=new_model_path,
                        project_info=project_info,
                        hyper_param_values=hyper_param_values,
                    )

                train_res = train(args)
                for callback in self.train_method_callbacks:
                    callback(args)

            try:
                f = open(new_model_path)
                f.close()
                logger.info(
                    f"({project_key}-{datasource_key}) Uploading round ({current_round}) trained model..."
                )
                project.push_model(new_model_path, datasource_key, params=train_res)
                logger.info("Done.")
            except FileNotFoundError:
                # no file saved by train()
                pass

    # creates a new datasource in the api
    def attach_datasource(self, key, train=None, test=None, name=None, metadata=None):
        while not self.instance_id:
            sleep(0.1)

        self.update_datasource(key, name, metadata)
        ds = _Datasource(key, api=self.datasource_api)
        self.datasources[key] = ds

        ds.add_trainer(DEFAULT_TRAINER_NAME, train=train, test=test)

        return ds

    def update_datasource(self, key, name=None, metadata=None):
        params = {"key": key, "instanceId": self.instance_id}
        if name is not None:
            params["name"] = name
        if self.metadata is not None:
            params["metadata"] = self.metadata
        if metadata is not None:
            params["metadata"] = metadata

        res = self.datasource_api.put_datasource(key, params)
        if res:
            logger.info(f'Updated datasource "{key}"')
        else:
            logger.info(f'Created datasource "{key}"')

    def delete_datasource(self, key):
        return self.datasource_api.delete_datasource(key)

    def delete_project(self, key):
        return _Project(key, api=self.project_api).delete_project()

    def get_user(self):
        return self.request._make_request("GET", "/user")

    def create_project(self, base_file, params, dynamic_trainer_path=None):
        project_obj = self.project_api.create_project(params=params)
        project = _Project(key=project_obj["key"], api=self.project_api)
        project.push_model(base_file, None)

        if dynamic_trainer_path:
            project.upload_file(dynamic_trainer_path)

        return project

    def create_centralized_project(self, name, compute, use_case=None, dataset=None):
        params = {
            "isCentralized": True,
            "name": name,
        }
        project_obj = self.project_api.create_project(params=params)
        project = _Project(key=project_obj["key"], api=self.project_api)

        if use_case:
            project.upload_file(use_case)

        project.add_datasource_and_trainer(compute, DEFAULT_TRAINER_NAME)

        return project

    def get_project(self, project_key: str):
        if not project_key:
            raise Exception("project_key cannot be empty or none")
        return _Project(key=project_key, api=self.project_api)

    def get_projects(self):
        projects = []
        project_info_list = self.project_api.get_projects()
        for project_info in project_info_list:
            projects.append(_Project(project_info["key"], api=self.project_api))
        return projects

    def get_datasources(self):
        return self.datasource_api.get_datasources()

    def is_datasource_labeled(self, project_key=None, datasource_key=None):
        """
        Accepts a valid project_key and datasource_key.
        Returns True if the datasource is labeled for the project; False otherwise

        """
        if not datasource_key or not project_key:
            raise Exception("project_key and datasource_key cannot be empty or None")

        try:
            bridge = self.project_api.get_bridge_of_project_and_datasource(
                project_key, datasource_key
            )

            if len(bridge["data"]) == 0:
                raise Exception("datasource_key not associated with this project")

            return bridge["data"][0].get("isLabelled", True)

        except Exception as e:
            logger.error("Something went wrong: {}".format(e))

    def get_use_cases(self):
        j = self.request._make_request("GET", "/useCases")
        if j:
            return j["data"]

    def get_datasets(self):
        j = self.request._make_request("GET", "/datasets")
        if j:
            return j["data"]

    def get_model(self, key: str):
        res = self.request._make_request("GET", f"/model/{key}")
        return res["data"]


def get_federated_path(project_key, base, ext, ds, round):
    return f"{base}/federated_model_{project_key}_{ds}_{round}.{ext}"


def get_trained_path(project_key, base, ext, ds, round):
    return f"{base}/trained_model_{project_key}_{ds}_{round}.{ext}"
