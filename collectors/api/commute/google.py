from dataclasses import dataclass, field
from typing import Dict

from collectors.api.commute.base import CommuteAPI, CommuteRequest


@dataclass
class GoogleAPIConfig:
    api_key: str
    region: str = field(default=None)
    mode: str = field(default='transit')
    arrival_time: str = field(default='now')


class GoogleCommuteAPI(CommuteAPI):
    config: GoogleAPIConfig = GoogleAPIConfig('missing')
    config_key = 'google-commute-api'

    def __init__(self, config: Dict):
        self.config.api_key = config[self.config_key]['api_key']

        for key in ['region', 'mode', 'arrival_time']:
            if key in config[self.config_key]:
                setattr(self.config, key, config[self.config_key][key])

    def check_commute_time(self, request: CommuteRequest) -> int:
        pass

    def normalize_address(self, address: str) -> str:
        return address