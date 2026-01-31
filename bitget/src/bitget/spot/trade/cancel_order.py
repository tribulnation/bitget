from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class CancelOrderData(TypedDict):
  orderId: str
  clientOid: str

validate_response = validator(CancelOrderData)

@dataclass
class CancelOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def cancel_order(
    self,
    symbol: str,
    *,
    order_id: str | None = None,
    client_oid: str | None = None,
    validate: bool | None = None
  ) -> CancelOrderData:
    """Cancel Order

    Either order_id or client_oid is required.

    - `symbol`: Trading pair, e.g. USDCUSDT.
    - `order_id`: Order ID.
    - `client_oid`: Client order ID.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Cancel-Order)
    """
    json_body: dict = {'symbol': symbol}
    if order_id is not None:
      json_body['orderId'] = order_id
    if client_oid is not None:
      json_body['clientOid'] = client_oid
    r = await self.authed_request('POST', '/api/v2/spot/trade/cancel-order', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
