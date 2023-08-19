import logging


class Test:
    def __init__(
        self,
        request,
        name: str,
        model_key: str,
        dataset_id: str,
        attack: str,
        gpu: object,
        config: list,
    ) -> None:
        self.request = request
        self.name = name
        self.model_key = model_key
        self.dataset_id = dataset_id
        self.attack = attack
        self.gpu = gpu
        self.config = config
        self.logger = logging.getLogger("Test")

        params = {
            "name": name,
            "modelKey": model_key,
            "datasetId": dataset_id,
            "attack": attack,
            "gpu": gpu,
            "config": config,
        }
        res = self.request._make_request("POST", "/attack/test", params=params)
        self.logger.info("Test created: {}".format(res))
