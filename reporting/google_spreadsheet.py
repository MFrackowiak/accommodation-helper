from dataclasses import dataclass, field
from typing import Optional

from collectors.scrappers.base import ParsedAccommodation
from reporting.base import CrawlingReporter


@dataclass
class GoogleSpreadsheetReporterConfig:
    oauth_storage: str
    spreadsheet_id: str
    scopes: str = field(default='https://www.googleapis.com/auth/spreadsheets')


class GoogleSpreadsheetCrawlingReporter(CrawlingReporter):
    def __init__(self, config: Optional[GoogleSpreadsheetReporterConfig],
                 **kwargs):
        self.config = config or GoogleSpreadsheetReporterConfig(**kwargs)

    def report_property_to_verify(self, advertisement: ParsedAccommodation,
                                  acceptor: str, reason: str):
        pass

    def report_property_accepted(self, advertisement: ParsedAccommodation,
                                 sent_email: bool):
        pass

