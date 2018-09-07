from typing import Optional


class AdvertisedProperty:
    def __init__(self, url: str, address: str, price: int, provided_by: str,
                 row: Optional[int]=None, commute: int=0, flagged: bool = False,
                 sent_email: bool=False):
        self.row = row
        self.url = url
        self.address = address
        self.price = price
        self.commute = commute
        self.flagged = flagged
        self.sent_email = sent_email
        self.provided_by = provided_by
