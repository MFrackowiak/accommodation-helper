from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from typing import Optional


@dataclass
class CommuteRequest:
    from_address: str
    to_address: str
    clean_from: bool = field(default=True)
    clean_to: bool = field(default=True)


class CommuteAPI(ABC):
    @abstractmethod
    def check_commute_time(self, request: CommuteRequest) -> Optional[int]:
        pass
