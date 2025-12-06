from dataclasses import dataclass

from .futures_transaction_records import FuturesTransactionRecords
from .margin_transaction_records import MarginTransactionRecords
from .spot_transaction_records import SpotTransactionRecords

@dataclass
class Tax(
  FuturesTransactionRecords,
  MarginTransactionRecords,
  SpotTransactionRecords,
):
  ...