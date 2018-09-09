from dataclasses import field, dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AdvertisedProperty:
    url: str
    address: str
    price: int
    provided_by: str
    entered: datetime
    ok: bool
    property_id: Optional[int] = field(default=None)
    row: Optional[int] = field(default=None)
    flagged: bool = field(default=False)
    sent_email: bool = field(default=False)