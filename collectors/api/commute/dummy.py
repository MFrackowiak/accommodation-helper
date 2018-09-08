from typing import Optional

from collectors.api.commute.base import CommuteRequest, CommuteAPI


class DummyCommuteAPI(CommuteAPI):
    def check_commute_time(self, request: CommuteRequest) -> Optional[int]:
        from_address = request.from_address.lower()
        if 'nice' in from_address:
            return 50
        elif 'rath' in from_address:
            return 40
        elif 'expensive' in from_address:
            return 20
        elif 'close' in from_address:
            return 10
        return None
