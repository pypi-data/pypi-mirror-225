'''
API wrapper for TronGrid.
'''
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pendulum
from pendulum import DateTime

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import is_contract_address
from trongrid_extractoor.helpers.csv_helper import *
from trongrid_extractoor.helpers.string_constants import *
from trongrid_extractoor.helpers.time_helpers import *
from trongrid_extractoor.models.trc20_txn import Trc20Txn
from trongrid_extractoor.models.tron_event import TronEvent
from trongrid_extractoor.progress_tracker import ProgressTracker
from trongrid_extractoor.request_params import MAX_TRADES_PER_CALL, RequestParams
from trongrid_extractoor.response import Response

RESCUE_DURATION_WALKBACK_SECONDS = [
    20,
    200,
    1000,
]

ONE_SECOND_MS = 1000.0
EMPTY_RESPONSE_RETRY_AFTER_SECONDS = 60

# Currently we poll from the most recent to the earliest events which is perhaps non optimal
ORDER_BY_BLOCK_TIMESTAMP_ASC = 'block_timestamp,asc'
ORDER_BY_BLOCK_TIMESTAMP_DESC = 'block_timestamp,desc'


class Api:
    def __init__(self, network: str = MAINNET, api_key: str = '') -> None:
        network = '' if network == MAINNET else f".{network}"
        self.base_uri = f"https://api{network}.trongrid.io/v1/"
        self.api_key = api_key

    def events_for_token(
            self,
            contract_addr: Optional[str] = None,
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None,
            output_dir: Optional[Path] = Path(''),
            filename_suffix: Optional[str] = None,
            resume_csv: Optional[Path] = None,
            event_name: str = 'Transfer'
        ) -> Path:
        """
        Get events by contract address and write to CSV. This is the endpoint that actually works
        to get all transactions (unlike the '[CONTRACT_ADDRESS]/transactions' endpoint).

          - contract_addr:   On-chain address of the token
          - since:           Start time to retrieve
          - until:           Start time to retrieve
          - output_dir:      Directory to write the CSV to
          - filename_suffix: Optional string to append to the filename
          - resume_csv:      Path to a CSV you want to resume writing
          - event_name:      Type of event to retrieve

        Test harness: https://developers.tron.network/v4.0/reference/events-by-contract-address
        """
        # Resume from CSV if requested
        if resume_csv is None and not is_contract_address(contract_addr):
            raise ValueError(f"Must provide a valid contract address or a CSV to resume.")

        resume_from_csv = resume_csv is not None
        output_path = resume_csv or output_csv_path(contract_addr, output_dir, filename_suffix)
        progress_tracker = ProgressTracker(output_path, resume_from_csv, contract_addr)
        contract_addr = contract_addr or progress_tracker.token_address
        log.info(f"Output CSV: '{output_path}'")

        if event_name == TRANSFER:
            event_cls = Trc20Txn
        else:
            log.warning(f"Not looking at {TRANSFER} events so dumping to json...")
            output_path = output_path.with_suffix('.json')
            event_cls = TronEvent

        # Setup params
        contract_url = f"{self.base_uri}contracts/{contract_addr}/events"
        params = RequestParams(contract_url, since, until, event_name=event_name)
        params.max_timestamp = progress_tracker.earliest_timestamp_seen() or params.max_timestamp

        # Start retrieving
        response = Response.get_response(contract_url, params.request_params())
        retrieved_txns = event_cls.extract_from_events(response.response)
        retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)
        write_rows(output_path, retrieved_txns)

        while response.is_continuable_response():
            if response.next_url() is not None:
                # Pull the next record
                response = Response.get_response(response.next_url())
            else:
                response.pretty_print()
                raise ValueError("Unparseable response!")

            retrieved_txns = event_cls.extract_from_events(response.response)
            retrieved_txns = progress_tracker.remove_already_processed_txns(retrieved_txns)
            write_rows(output_path, retrieved_txns)

            if response.is_paging_complete():
                log.info(f"Paging complete for {params} so will end loop...")

        log.info(f"Extraction complete. Wrote {progress_tracker.number_of_rows_written()} new rows to '{output_path}'.")
        log.info(f"    Lowest block_number seen:  {progress_tracker.min_block_number_seen}")
        log.info(f"    Highest block_number seen: {progress_tracker.max_block_number_seen}")
        log.info(f"Here is the last response from the api for params: {params}")
        response.print_abbreviated()
        return output_path

    def trc20_xfers_for_wallet(self, contract_addr: str, wallet_addr: str, token_type: str = TRC20) -> List[Trc20Txn]:
        """Use the TRC20 endpoint to get transfers for a particular wallet/token combo."""
        raise NotImplementedError("Needs revision to use ProgressTracker and more.")
        wallet_url = f"{self.base_uri}accounts/{wallet_addr}/transactions/{token_type}"
        params = Api.build_params(extra={'contract_address': contract_addr})
        response = Response.get_response(wallet_url, params)
        txns = Trc20Txn.extract_from_wallet_transactions(response)

        while META in response and 'links' in response[META]:
            if DATA not in response or len(response[DATA]) == 0:
                break

            min_timestamp = min([tx.ms_from_epoch for tx in txns])
            params[MAX_TIMESTAMP] = min_timestamp
            response = Response.get_response(wallet_url, params)
            txns.extend(Trc20Txn.extract_from_wallet_transactions(response))

        unique_txns = Trc20Txn.unique_txns(txns)
        log.info(f"Extracted a total of {len(txns)} txns ({len(unique_txns)} unique txns).")
        return unique_txns
