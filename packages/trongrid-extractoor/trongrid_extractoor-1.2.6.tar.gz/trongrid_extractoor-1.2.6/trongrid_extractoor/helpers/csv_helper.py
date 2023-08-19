import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pendulum
from rich.pretty import pprint

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import *
from trongrid_extractoor.models.trc20_txn import CSV_FIELDS, Trc20Txn

WRITTEN = 'written'
WRITTEN_AT_REGEX = re.compile(WRITTEN + "_(\\d{4}-\\d{2}-\\d{2}T\\d{2}[.:]\\d{2}[.:]\\d{2})\\.csv")


# TODO: The handoff between json or csv is kind of janky
def write_rows(file_path: Union[str, Path], rows: List[Any]) -> None:
    """Wrote the rows either as CSV (if Trc20Txn objs) or just dump to JSON"""
    file_mode = 'a' if Path(file_path).exists() else 'w'

    if len(rows) == 0:
        logging.warning(f"Nothing write to '{file_path}'...")
        return

    # Trc20Txns are written as CSVs
    if type(rows[0]) == Trc20Txn:
        _write_txn_rows(file_path, rows, file_mode)
        return

    # Otherwise we are just writing JSON
    with open(file_path, file_mode) as output_file:
        rows = [row.raw_event for row in rows]
        json.dump(rows, output_file, indent=3)


def read_json(file_path: Path) -> List[Dict[str, Any]]:
    """JSON is dumped as a series of arrays so we need to turn the string into a single array."""
    with open(file_path, 'r') as file:
        return json.loads(file.read().replace('][', ','))


def output_csv_path(address: str, dir: Optional[Path] = None, suffix: Optional[str] = None) -> Path:
    """Build a filename that contains the address and (if available) the symbol."""
    dir = dir or Path('')
    filename = csv_prefix(address)

    if suffix:
        filename += f"__{suffix}"

    # TODO: stop replacing the ':'
    filename += csv_suffix()
    return dir.joinpath(filename.replace(':', '.').replace('/', '.'))


def load_csv(csv_path: Union[str, Path]) -> List[Dict[str, Any]]:
    with open(Path(csv_path), mode='r') as csvfile:
        return [
            row
            for row in csv.DictReader(csvfile, delimiter=',')
        ]


def csvs_with_prefix_in_dir(dir: Union[str, Path], prefix: str) -> List[str]:
    return [f.name for f in Path(dir).glob(f"{prefix}*.csv")]


def csv_prefix(address: str) -> str:
    filename = 'events_'

    if is_contract_address(address):
        symbol = symbol_for_address(address)
    else:
        symbol = address
        address = address_of_symbol(address)

        if not address:
            raise ValueError(f"No address found for {symbol}!")

    if symbol:
        filename += f"{symbol}_"

    filename += address
    return filename


def csv_suffix() -> str:
    """String showing the time the file was created."""
    return f"__{WRITTEN}_{datetime.now().strftime('%Y-%m-%dT%H.%M.%S')}.csv"


def parse_written_at_from_filename(csv_path: Union[str, Path]) -> pendulum.DateTime:
    """Extract the written timestmap (output of csv_suffix()) to a timestamp."""
    match = WRITTEN_AT_REGEX.search(str(csv_path))

    if match is None:
        raise ValueError(f"'{csv_path}' does not seem to have an embedded written_at timestamp!")

    return pendulum.parse(match.group(1).replace('.', ':'))


def _write_txn_rows(file_path: Union[str, Path], rows: List[Trc20Txn], file_mode: str) -> None:
    log.info(f"Writing {len(rows)} txn rows to CSV...")

    with open(file_path, file_mode) as f:
        csv_writer = csv.DictWriter(f, CSV_FIELDS)

        if file_mode == 'w':
            csv_writer.writeheader()

        # Put this after the header is written so there is always an output file
        if len(rows) == 0:
            log.warning(f"No rows to write!")
            return

        csv_writer.writerows([row.as_dict(CSV_FIELDS) for row in rows])
