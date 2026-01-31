from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class UnfilledOrderItem(TypedDict):
  userId: str
  symbol: str
  orderId: str
  clientOid: str
  priceAvg: Decimal
  size: Decimal
  orderType: Literal['limit', 'market']
  side: Literal['buy', 'sell']
  status: Literal['live', 'partially_filled', 'filled', 'cancelled']
  basePrice: Decimal
  baseVolume: Decimal
  quoteVolume: Decimal
  enterPointSource: str
  cTime: Timestamp
  uTime: Timestamp

validate_response = validator(list[UnfilledOrderItem])

@dataclass
class UnfilledOrders(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def unfilled_orders(
    self,
    *,
    symbol: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    id_less_than: str | None = None,
    order_id: str | None = None,
    validate: bool | None = None
  ) -> list[UnfilledOrderItem]:
    """Get Current (Unfilled) Orders

    - `symbol`: Trading pair.
    - `start`, `end`: Time range (max 90 days).
    - `limit`: Default 100, max 100.
    - `id_less_than`: Pagination, orderId.
    - `order_id`: Filter by order ID.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Get-Unfilled-Orders)
    """
    params: dict = {}
    if symbol is not None:
      params['symbol'] = symbol
    if start is not None:
      params['startTime'] = ts.dump(start)
    if end is not None:
      params['endTime'] = ts.dump(end)
    if limit is not None:
      params['limit'] = limit
    if id_less_than is not None:
      params['idLessThan'] = id_less_than
    if order_id is not None:
      params['orderId'] = order_id
    r = await self.authed_request('GET', '/api/v2/spot/trade/unfilled-orders', params=params)
    return self.output(r.text, validate_response, validate=validate)
