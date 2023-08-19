import logging

from .attacks import pii_extraction
from .datasets import dataset
from .logging import set_logger
from .MessageHandler import _MessageHandler
from .models import local_model
from .State import _State
from .tests import test

RETRY_AFTER = 5  # seconds


class DynamoFL:
    """Creates a client instance that communicates with the API through REST and websockets.
    ### Parameters
        token - Your auth token. Required.

        host - API server url. Defaults to DynamoFL prod API.

        metadata - Sets a default metadata object for attach_datasource calls; can be overriden.

        log_level - Set the log_level for the client. Accepts all of logging._Level. Defaults to logging.INFO.
    """

    def __init__(
        self,
        token: str,
        host: str = "https://api.dynamofl.com",
        metadata: object = None,
        log_level=logging.INFO,
    ):
        self._state = _State(token, host, metadata)
        self._messagehandler = _MessageHandler(self._state)
        self._messagehandler.connect_to_ws()

        set_logger(log_level=log_level)

    def attach_datasource(self, key, train=None, test=None, name=None, metadata=None):
        return self._state.attach_datasource(
            key, train=train, test=test, name=name, metadata=metadata
        )

    def delete_datasource(self, key):
        return self._state.delete_datasource(key)

    def get_datasources(self):
        return self._state.get_datasources()

    def delete_project(self, key):
        return self._state.delete_project(key)

    def get_user(self):
        return self._state.get_user()

    def create_project(self, base_model_path, params, dynamic_trainer_path=None):
        return self._state.create_project(
            base_model_path, params, dynamic_trainer_path=dynamic_trainer_path
        )

    def get_project(self, project_key):
        return self._state.get_project(project_key)

    def get_projects(self):
        return self._state.get_projects()

    def is_datasource_labeled(self, project_key=None, datasource_key=None):
        """
        Accepts a valid datasource_key and project_key
        Returns True if the datasource is labeled for the project; False otherwise

        """
        return self._state.is_datasource_labeled(
            project_key=project_key, datasource_key=datasource_key
        )

    def create_attack(self):
        return pii_extraction.PIIExtraction(self._state.request)

    def get_model(self, model_id: str):
        return pii_extraction.PIIExtraction(self._state.request)

    def create_test(
        self,
        name: str,
        model_key: str,
        dataset_id: str,
        attack: str,
        gpu: object,
        config: list,
    ):
        return test.Test(
            request=self._state.request,
            name=name,
            model_key=model_key,
            dataset_id=dataset_id,
            attack=attack,
            gpu=gpu,
            config=config,
        )

    def get_use_cases(self):
        self._state.get_use_cases()

    def get_datasets(self):
        self._state.get_datasets()

    def create_centralized_project(self, name, compute, use_case=None, dataset=None):
        self._state.create_centralized_project(name, compute, use_case, dataset)

    def create_model(
        self,
        key: str,
        model_file_path: str,
        name: str,
        config: object,
        dataset_file_path: str = None,
    ):
        return local_model.LocalModel(
            request=self._state.request,
            name=name,
            key=key,
            model_file_path=model_file_path,
            dataset_file_path=dataset_file_path,
            config=config,
        )

    def get_model(self, key: str):
        return self._state.get_model(key)

    def create_dataset(self, key: str, file_path, name: str = ""):
        return dataset.Dataset(
            request=self._state.request, name=name, key=key, file_path=file_path
        )
