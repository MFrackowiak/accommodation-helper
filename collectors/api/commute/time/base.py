from abc import abstractmethod, ABC
from datetime import datetime
from pytz import timezone


class ConfigurationTimeParser(ABC):
    def __init__(self, tz_name: str):
        self.tz_info = timezone(tz_name)

    @abstractmethod
    def parse_time(self, string_to_parse: str) -> datetime:
        pass