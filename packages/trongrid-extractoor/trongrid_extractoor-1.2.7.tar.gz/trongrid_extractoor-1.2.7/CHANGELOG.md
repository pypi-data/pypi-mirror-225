# NEXT RELEASE

### 1.2.7
* Add missing `exceptions.py`

### 1.2.6
* Standardize rounding of floats to ints

### 1.2.5
* Retry rate limit exceeded errors
* Fix warning message in ms_to_datetime

### 1.2.4
* Log a warning that includes the duplicate transaction id if duplicates are encountered

### 1.2.3
* Add symbol shorthand for many tokens

### 1.2.2
* Truncate the `.0` off of the `amount` and `ms_from_epoch` column (turn them to integers, which is what they actually are)

### 1.2.1
* Two underscores between each section of csv filename

# 1.2.0
* Add `--event-name` argument to CLI (and API)
* Allow pulling of all events with `--event-name None`
* Events other than `Transfer` write to JSON
* Rename `extract_tron_transactions` to `extract_tron_events`

# 1.1.0
* Add `parse_written_at_from_filename()` method
* `TCNH` and `wstUSDT` token shorthand

# 1.0.0
* As of mid July 2023 TronGrid seems to have repaired their API so it no longer just gives up after returning 5 pages of responses. This dramatically simplifies the code in this package.
* Guarantee there is always a CSV with a header row at the end even if there's no rows returned by query.
* enable `jUSDC` and `stUSDT` token shorthand symbols

# 0.4.0
* `--resume` option automatically determines the token address from the CSV
* `--debug` option for `extract_tron_transactions` CLI
* `--list-symbols` option for `extract_tron_transactions` CLI
* Accept command line args without timezone (assume UTC)
* Log count of rows extracted.
* Fix crash when throwing error about unable to resume from CSV

### 0.3.12
* `RequestParams` class, better logging

### 0.3.11
* Only use Rich formatted logging when running with the CLI

### 0.3.10
* Reduce verbosity of logged writes

### 0.3.9
* Don't consider small timespan queries failures in need of rescuing if they return 0 rows.

### 0.3.8
* Fix buggy handling of false completes

### 0.3.7
* Delete output CSV if it already exists
* Fix bug with resuming from CSV with out of order rows
* Only do a rescue when it is impossible to load next page
* Add a bunch of tokens (`HT`, `SUN`, `JST`, `BTT`, etc.)

### 0.3.6
* Simplify inner logic and retries etc.

### 0.3.5
* Avoid endless loop on `is_false_complete_response()`
* Refactor `response.pretty_print()`
* Don't allow walkbacks to walk back past the start of the period

### 0.3.4
* `Response` object refactor
* Smarter logging
* Strip `:` and `/` from CSV filenames

### 0.3.3
* Add `filename_suffix` arg

### 0.3.2
* Tidbits

### 0.3.1
* Better 0 txn response handling
* `compile_csvs.py` script

# 0.3.0
* `--resume-csv` option
* Use floats instead of strings for timestamps. Add `_is_paging_complete()` method
* Handle src/dst/wad txns

# 0.2.0
* `ProgressTracker` class
* `event_number` column
* Accept symbols like `USDT` as argument instead of just addresses
* Accept `--since`, `--until`, and `--output-dir` options on the command line

# 0.1.0
* Initial release.
