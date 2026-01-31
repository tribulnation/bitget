from typing_extensions import Literal
from datetime import datetime, timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class MarketTradeItem(TypedDict):
  symbol: str
  tradeId: str
  side: Literal['buy', 'sell', 'Buy', 'Sell']  # API returns capitalized
  price: Decimal
  size: Decimal
  ts: Timestamp

validate_response = validator(list[MarketTradeItem])

@dataclass
class MarketTrades(Endpoint):
  @rate_limit(timedelta(seconds=1/10))
  async def market_trades(
    self,
    symbol: str,
    *,
    limit: int | None = None,
    id_less_than: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    validate: bool | None = None
  ) -> list[MarketTradeItem]:
    """Get Market Trades

    Data within 90 days. startTime and endTime must be within 7 days.

    - `symbol`: Trading pair name, e.g. BTCUSDT.
    - `limit`: Default 500, max 1000.
    - `id_less_than`: Returns records less than this tradeId.
    - `start`, `end`: Time range (max 7 days).
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-Market-Trades)
    """
    params: dict = {'symbol': symbol}
    if limit is not None:
      params['limit'] = limit
    if id_less_than is not None:
      params['idLessThan'] = id_less_than
    if start is not None:
      params['startTime'] = ts.dump(start)
    if end is not None:
      params['endTime'] = ts.dump(end)
    r = await self.request('GET', '/api/v2/spot/market/fills-history', params=params)
    return self.output(r.text, validate_response, validate=validate)
