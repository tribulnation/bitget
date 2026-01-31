from typing_extensions import Literal
from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class PlaceOrderData(TypedDict):
  orderId: str
  clientOid: str

validate_response = validator(PlaceOrderData)

@dataclass
class PlaceOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def place_order(
    self,
    symbol: str,
    side: Literal['buy', 'sell'],
    order_type: Literal['limit', 'market'],
    size: str,
    *,
    force: Literal['gtc', 'post_only', 'fok', 'ioc'] | None = None,
    price: str | None = None,
    client_oid: str | None = None,
    validate: bool | None = None
  ) -> PlaceOrderData:
    """Place Order

    - `symbol`: Trading pair, e.g. USDCUSDT.
    - `side`: buy / sell.
    - `order_type`: limit / market.
    - `size`: For limit and market-sell = base coins. For market-buy = quote coins.
    - `force`: gtc, post_only, fok, ioc (invalid when order_type is market).
    - `price`: Limit price (required for limit).
    - `client_oid`: Client order ID.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Place-Order)
    """
    json_body: dict = {'symbol': symbol, 'side': side, 'orderType': order_type, 'size': size}
    if order_type == 'limit':
      json_body['force'] = force or 'gtc'
      if price is not None:
        json_body['price'] = price
    if client_oid is not None:
      json_body['clientOid'] = client_oid
    r = await self.authed_request('POST', '/api/v2/spot/trade/place-order', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
