from datetime import timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp

class OrderbookData(TypedDict):
  asks: list[list[Decimal]]
  bids: list[list[Decimal]]
  ts: Timestamp

validate_response = validator(OrderbookData)

@dataclass
class Orderbook(Endpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def orderbook(
    self,
    symbol: str,
    *,
    depth_type: str | None = None,
    limit: int | None = None,
    validate: bool | None = None
  ) -> OrderbookData:
    """Get OrderBook Depth

    - `symbol`: Trading pair.
    - `depth_type`: step0, step1, step2, step3, step4, step5. Default step0.
    - `limit`: Default 150, maximum 150.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-Orderbook)
    """
    params: dict = {'symbol': symbol}
    if depth_type is not None:
      params['type'] = depth_type
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v2/spot/market/orderbook', params=params)
    return self.output(r.text, validate_response, validate=validate)
