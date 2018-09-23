from dataclasses import dataclass, field
from typing import Dict

from googlemaps.client import Client
from googlemaps.directions import directions

from collectors.api.commute.base import CommuteAPI, CommuteRequest
from collectors.api.commute.time.simple import SimpleConfigurationTimeParser
from utils.datetime_utils import timestamp_from_datetime


@dataclass
class GoogleAPIConfig:
    api_key: str
    region: str = field(default=None)
    mode: str = field(default='transit')
    arrival_time: str = field(default='now')
    parse_arrival_time: bool = field(default=False)
    arrival_time_timezone: str = field(default='UTC')


class GoogleCommuteAPI(CommuteAPI):
    config_key = 'google-commute-api'

    def __init__(self, config: Dict):
        self.config: GoogleAPIConfig = GoogleAPIConfig(
            **config[self.config_key],
        )
        self.client: Client = Client(self.config.api_key)

    def check_commute_time(self, request: CommuteRequest) -> int:
        directions_dict = directions(
            self.client,
            origin=request.from_address,
            destination=request.to_address,
            mode=self.config.mode,
            units='metric',
            language='en',
            region=self.config.region,
            **self._get_times(),
        )

    def _get_times(self) -> Dict[str, str]:
        if self.config.parse_arrival_time:
            time_parser = SimpleConfigurationTimeParser(
                self.config.arrival_time_timezone)
            return {'arrival_time':
                timestamp_from_datetime(
                    time_parser.parse_time(self.config.arrival_time))}
        return {'arrival_time': self.config.arrival_time}

    def normalize_address(self, address: str) -> str:
        return address
