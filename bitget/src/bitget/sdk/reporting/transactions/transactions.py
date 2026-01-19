from typing_extensions import AsyncIterable, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from trading_sdk.reporting import Transactions as _Transactions, Transaction

from bitget.sdk.core import SdkMixin
from .spot import SpotTransactions
from .futures import FutureTransactions
from .margin import MarginTransactions

@dataclass
class Transactions(SdkMixin, _Transactions):
  unkwown_types_as_other: bool = field(kw_only=True, default=True)

  def __post_init__(self):
    self.spot_transactions = SpotTransactions(self.client, unkwown_types_as_other=self.unkwown_types_as_other)
    self.future_transactions = FutureTransactions(self.client, unkwown_types_as_other=self.unkwown_types_as_other)
    self.margin_transactions = MarginTransactions(self.client, unkwown_types_as_other=self.unkwown_types_as_other)

  async def _transactions_impl(self, start: datetime, end: datetime) -> AsyncIterable[Sequence[Transaction]]:
    async for chunk in self.spot_transactions(start, end):
      yield chunk
    async for chunk in self.future_transactions(start, end):
      yield chunk
    async for chunk in self.margin_transactions(start, end):
      yield chunk