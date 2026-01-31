from typing_extensions import Literal
from datetime import timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp

class RecentTradeItem(TypedDict):
  symbol: str
  tradeId: str
  side: Literal['buy', 'sell', 'Buy', 'Sell']  # API may return capitalized
  price: Decimal
  size: Decimal
  ts: Timestamp

validate_response = validator(list[RecentTradeItem])

@dataclass
class RecentTrades(Endpoint):
  @rate_limit(timedelta(seconds=1/10))
  async def recent_trades(
    self,
    symbol: str,
    *,
    limit: int | None = None,
    validate: bool | None = None
  ) -> list[RecentTradeItem]:
    """Get Recent Trades

    - `symbol`: Trading pair name, e.g. BTCUSDT.
    - `limit`: Default 100, max 500.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-Recent-Trades)
    """
    params: dict = {'symbol': symbol}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v2/spot/market/fills', params=params)
    return self.output(r.text, validate_response, validate=validate)
