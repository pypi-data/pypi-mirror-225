from typing import List

from requests import Session

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler


class Frames(AbstractHandler):
    def __init__(
        self,
        session: Session,
        dataset_id: str = None,
    ):
        self.route = f'{MainConfig.main_url}/dataset/{dataset_id}/'
        super().__init__(session)

    def read_meta(self, part_of_dataset: str):
        self._get(self.route + f'/{part_of_dataset}/frames/meta', stream=True)
        return self.send()

    @AbstractHandler.pos_val
    def create_fb(self, *args, files: List[bytes]):
        self._post(self.route, files=files)
        return self.send()
