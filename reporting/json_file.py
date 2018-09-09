from dataclasses import dataclass, asdict
from json import load, dump
from os import path
from typing import Optional, List, Dict

from collectors.scrappers.base import ParsedAccommodation
from reporting.base import CrawlingReporter


@dataclass
class JsonCrawlingReporterConfig:
    filename: str
    always_save_and_close: bool


class JsonCrawlingReporter(CrawlingReporter):
    class StorageFile:
        def __init__(self, filename):
            self.filename = filename
            self.data = {'accepted': [], 'verify': []}

        def __enter__(self):
            if path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    self.data = load(file) or {'accepted': [], 'verify': []}
            else:
                self.data = {'accepted': [], 'verify': []}
            return self.data

        def __exit__(self, *args):
            with open(self.filename, 'w') as file:
                dump(self.data, file)

    def __init__(self, config: Optional[JsonCrawlingReporterConfig], **kwargs):
        self.config: JsonCrawlingReporterConfig = config or \
                                                  JsonCrawlingReporterConfig(
                                                      **kwargs)
        self.storage_file = self.StorageFile(self.config.filename)

    def report_property_to_verify(self, advertisement: ParsedAccommodation,
                                  acceptor: str, reason: str) -> int:
        if self.config.always_save_and_close:
            with self.storage_file as data:
                self._report_property_to_verify(
                    data['verify'], advertisement, acceptor, reason)
        else:
            self._report_property_to_verify(self.storage_file.data['verify'])
        return len(self.storage_file.data['verify'])

    def _report_property_to_verify(
            self, verify_list: List[Dict], advertisement: ParsedAccommodation,
            acceptor: str, reason: str):
        verify_list.append(dict(
            **asdict(advertisement),
            acceptor=acceptor,
            reason=reason,
        ))

    def report_property_accepted(self, advertisement: ParsedAccommodation,
                                 sent_email: bool) -> int:
        if self.config.always_save_and_close:
            with self.storage_file as data:
                self._report_property_to_verify(
                    data['verify'], advertisement, sent_email)
        else:
            self._report_property_to_verify(self.storage_file.data['verify'])
        return len(self.storage_file.data['verify'])

    def _report_property_accepted(
            self, accept_list: List[Dict], advertisement: ParsedAccommodation,
            sent_email: bool):
        accept_list.append(dict(
            **asdict(advertisement),
            sent_email=sent_email,
        ))
