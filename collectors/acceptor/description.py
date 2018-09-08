from dataclasses import dataclass, field
from re import compile as re_compile, sub
from typing import Optional, List, Dict, Tuple

from collectors.acceptor.base import Acceptor, AcceptorResponse
from collectors.scrappers.scrapper import ParsedAccommodation


@dataclass
class DescriptionConfig:
    reject_if_found: List[Dict[str, str]] = field(default=())
    verify_if_found: List[Dict[str, str]] = field(default=())


@dataclass
class ParsedDescriptionConfig:
    reject_strings: List[Tuple[str]]
    reject_regexps: List[str]
    verify_strings: List[Tuple[str]]
    verify_regexps: List[str]


class DescriptionAcceptor(Acceptor):
    def __init__(self, config: Optional[DescriptionConfig], **kwargs):
        self.config = config or DescriptionConfig(**kwargs)

        if not (self.config.reject_if_found or self.config.verify_if_found):
            raise ValueError('Improperly Configured!')

        self._parsed_config = self._parse_config()

    def _parse_config(self) -> ParsedDescriptionConfig:
        return ParsedDescriptionConfig(
            *self._parse_config_list(self.config.reject_if_found),
            *self._parse_config_list(self.config.verify_if_found),
        )

    def _simple_clean(self, to_clean: str) -> str:
        return sub(
            '\s+', ' ', sub('[*,./"\'()@!?]', ' ', to_clean.lower())).strip()

    def _simple_tokenize(self, to_tokenize: str) -> List[str]:
        return to_tokenize.split()

    def _is_sublist(self, candidate_list: List[str],
                    source_list: List[str]) -> bool:
        candidate_len = len(candidate_list)
        source_len = len(source_list)

        if candidate_len > source_len:
            return False
        elif candidate_len == source_len:
            return candidate_list == source_list
        return any([
            candidate_list == source_list[i:i + candidate_len]
            for i in range(0, source_len - candidate_len + 1)
        ])

    def _parse_config_list(
            self, config_list: List[Dict[str, str]]) -> Tuple[List, List]:
        strings, regexps = [], []

        for check_dict in config_list:
            if check_dict.get('is_reg', False):
                regexps.append(re_compile(check_dict['phrase']))
            else:
                strings.append(
                    self._simple_tokenize(
                        self._simple_clean(check_dict['phrase'])))

        return strings, regexps

    def _check_regexps_and_strings(
            self, cleaned, tokens, regexps, strings) -> bool:
        test_regexps = any(map(lambda r: r.search(cleaned), regexps))
        test_strings = any(
            map(lambda s: self._is_sublist(s, tokens), strings))
        return test_regexps or test_strings

    def is_ok(self,
              found_property: ParsedAccommodation) -> AcceptorResponse:
        cleaned_description = self._simple_clean(found_property.description)
        token_description = self._simple_tokenize(cleaned_description)

        if self._check_regexps_and_strings(
                cleaned_description, token_description,
                self._parsed_config.reject_regexps,
                self._parsed_config.reject_strings
        ):
            return AcceptorResponse.REJECT
        elif self._check_regexps_and_strings(
                cleaned_description, token_description,
                self._parsed_config.verify_regexps,
                self._parsed_config.verify_strings
        ):
            return AcceptorResponse.VERIFY
        return AcceptorResponse.ACCEPT
