from typing_extensions import Literal
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class OrderInfoItem(TypedDict):
  userId: str
  symbol: str
  orderId: str
  clientOid: str
  price: Decimal
  size: Decimal
  orderType: Literal['limit', 'market']
  side: Literal['buy', 'sell']
  status: Literal['live', 'partially_filled', 'filled', 'cancelled']
  priceAvg: Decimal
  baseVolume: Decimal
  quoteVolume: Decimal
  enterPointSource: str
  feeDetail: str
  orderSource: str
  cancelReason: str
  cTime: Timestamp
  uTime: Timestamp

validate_response = validator(list[OrderInfoItem])

@dataclass
class OrderInfo(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def order_info(
    self,
    *,
    order_id: str | None = None,
    client_oid: str | None = None,
    validate: bool | None = None
  ) -> list[OrderInfoItem]:
    """Get Order Info

    Either order_id or client_oid is required.

    - `order_id`: Order ID.
    - `client_oid`: Client order ID.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Get-Order-Info)
    """
    params: dict = {}
    if order_id is not None:
      params['orderId'] = order_id
    if client_oid is not None:
      params['clientOid'] = client_oid
    r = await self.authed_request('GET', '/api/v2/spot/trade/orderInfo', params=params)
    return self.output(r.text, validate_response, validate=validate)
