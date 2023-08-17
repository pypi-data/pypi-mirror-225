"""
Wrapper for trongrid's response JSON data.
"""
import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Union

import requests
from requests_toolbelt.utils import dump
from rich.pretty import pprint
from tenacity import after_log, retry, stop_after_attempt, wait_exponential

from trongrid_extractoor.config import log
from trongrid_extractoor.request_params import RequestParams
from trongrid_extractoor.helpers.csv_helper import *
from trongrid_extractoor.helpers.string_constants import *
from trongrid_extractoor.helpers.time_helpers import *

# If the distance between min and max_timestamp is less than this don't consider a 0 row
# result a failure.
OK_DURATION_FOR_ZERO_TXNS_MS = 10000
JSON_HEADERS = {'Accept': 'application/json'}

TRONGRID_RETRY_KWARGS = {
    'wait': wait_exponential(multiplier=1, min=15, max=300),
    'stop': stop_after_attempt(5),
    'after': after_log(log, logging.DEBUG),
}


@dataclass
class Response:
    raw_response: requests.models.Response
    params: Dict[str, Any]

    def __post_init__(self):
        log.debug(dump.dump_all(self.raw_response).decode('utf-8'))
        self.response = self.raw_response.json()

    @classmethod
    @retry(**TRONGRID_RETRY_KWARGS)
    def get_response(
            cls,
            url: str,
            params: Optional[Dict[str, Union[str, int, float]]] = None
        ) -> 'Response':
        """Alternate constructor that calls the API with retries."""
        params = params or {}

        # If an API call yields too many rows to fit in one response a 'next URL' is given and
        # our requests use that URL without params.
        is_new_query = (MIN_TIMESTAMP in params) and (MAX_TIMESTAMP in params)

        # Min/Max timestamps are INCLUSIVE.
        if is_new_query:
            msg = f"Requesting data from {ms_to_datetime(params[MIN_TIMESTAMP])} " \
                  f"to {ms_to_datetime(params[MAX_TIMESTAMP])}."
            log.info(msg)

        log.debug(f"Request URL: {url}\nParams: {params}")
        raw_response = requests.get(url, headers=JSON_HEADERS, params=params)
        response = cls(raw_response, deepcopy(params))

        # Sometimes TronGrid will return 0 rows for no apparent reason. Retrying usually fixes it
        # so we throw an exception to get a tenacity retry.
        # It also seems that if the number of responses to a query is a multiple of 200 (the page sizez)
        # Trongrid may page through to an empty response. That case is not well handled here.
        if response.is_false_complete_response() and not is_new_query:
            log.warning("Empty response that perhaps should not be empty...")
            msg = f"Seems like an actual error: response shouldn't be empty. Response:\n{response.response}\n\nRetrying.."
            log.warning(msg)
            response.pretty_print()
            raise ValueError(msg)

        return response

    def is_continuable_response(self) -> bool:
        """Return True if the response contains a link to the next page via a url."""
        return self.next_url() is not None

    def is_paging_complete(self) -> bool:
        """Return True if it appears that we successfully paged to the end of the query."""
        page_size = self.page_size() or 0
        return self.was_successful() and page_size > 0 and self.next_url() is None

    def is_false_complete_response(self) -> bool:
        """Sometimes for no reason TronGrid just returns 0 rows to a query that would otherwise return rows."""
        return self.was_successful() and self.page_size() == 0 and self.next_url() is None

    def was_successful(self) -> bool:
        if SUCCESS not in self.response:
            log.warning(f"No '{SUCCESS}' key found in response!\n{self.response}")
            return False

        success = self.response[SUCCESS]

        if not isinstance(success, bool):
            raise ValueError(f"{success} is of type {type(success)} instead of bool!")

        return success

    def next_url(self) -> Optional[str]:
        """If the number of results is more than the page size Trongrid return a URL for the next page."""
        if META in self.response and LINKS in self.response[META] and NEXT in self.response[META][LINKS]:
            return self.response[META][LINKS][NEXT]

    def page_size(self) -> Optional[int]:
        """Extract the number of results returned in this page of results."""
        if META in self.response and PAGE_SIZE in self.response[META]:
            return self.response[META][PAGE_SIZE]

    def without_data(self) -> Dict[str, Any]:
        """Return the response JSON just without the 'data' field."""
        abbreviated_response = deepcopy(self.response)
        abbreviated_response['data'] = f"[Skipping {len(self.response['data'])} elements of 'data' array]"
        return abbreviated_response

    def pretty_print(self) -> None:
        log.info(f"RAW RESPONSE:")
        log.info(dump.dump_all(self.raw_response).decode('utf-8') + "\n")
        log.info(f"Response formatted with Rich:")
        pprint(self, expand_all=True)
        pprint(self.response, expand_all=True)

    def print_abbreviated(self) -> None:
        pprint(self.without_data(), expand_all=True)
