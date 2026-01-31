from datetime import timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp

class TickerItem(TypedDict):
  symbol: str
  high24h: Decimal
  open: Decimal
  lastPr: Decimal
  low24h: Decimal
  quoteVolume: Decimal
  baseVolume: Decimal
  usdtVolume: Decimal
  bidPr: Decimal
  askPr: Decimal
  bidSz: Decimal | None
  askSz: Decimal | None
  openUtc: Decimal
  ts: Timestamp
  changeUtc24h: Decimal
  change24h: Decimal

validate_response = validator(list[TickerItem])

@dataclass
class Tickers(Endpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def tickers(self, *, symbol: str | None = None, validate: bool | None = None) -> list[TickerItem]:
    """Get Ticker Information

    Supports both single and batch queries.

    - `symbol`: Trading pair name, e.g. BTCUSDT. If blank, all trading pair information is returned.
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-Tickers)
    """
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v2/spot/market/tickers', params=params)
    return self.output(r.text, validate_response, validate=validate)
