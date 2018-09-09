from typing import Optional, Dict

from collectors.api.commute.base import CommuteAPI, CommuteRequest
import re


class DublinPostcodeCommuteAPI(CommuteAPI):
    config_key = 'dublin-zip-commute-api'
    regexp = re.compile('dublin\s*(\d+w?)', re.RegexFlag.IGNORECASE)

    def __init__(self, config: Dict):
        self.config = config.get(self.config_key, {})

    def check_commute_time(self, request: CommuteRequest) -> Optional[int]:
        dublin_code = self.parse_dublin_code(request.from_address)
        if dublin_code:
            return self.config.get(dublin_code)
        return None

    def parse_dublin_code(self, address_str):
        try:
            return self.regexp.search(address_str).group(1).upper()
        except AttributeError:
            return None