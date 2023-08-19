import logging

from dynamofl.datasets.dataset import Dataset


class Model:
    def __init__(
        self,
        request,
        name: str,
        key: str,
        type: str,
        dataset_file_path: str = None,
        config: object = {},
    ) -> None:
        self.key = key
        self.name = name
        self.config = config
        self.request = request
        self.type = type
        self.logger = logging.getLogger("Model")

        params = {"key": key, "name": name, "config": config, "type": type}
        created_model = self.request._make_request("POST", "/ml-model", params=params)
        self._id = created_model["_id"]
        self.logger.info("Model created: ", created_model)
        if dataset_file_path:
            dataset = Dataset(request, key=key, name=name, file_path=dataset_file_path)
            self.attach_dataset(dataset)
            self.dataset = dataset
