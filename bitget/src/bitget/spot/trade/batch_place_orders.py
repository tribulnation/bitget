from typing_extensions import Literal, NotRequired
from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class BatchOrderInput(TypedDict):
  side: Literal['buy', 'sell']
  orderType: Literal['limit', 'market']
  size: str
  symbol: NotRequired[str]  # required in multiple batch_mode only
  price: NotRequired[str]
  force: NotRequired[Literal['gtc', 'post_only', 'fok', 'ioc']]
  clientOid: NotRequired[str]

class BatchPlaceOrderSuccessItem(TypedDict):
  orderId: str
  clientOid: str

class BatchPlaceOrderFailureItem(TypedDict):
  orderId: str
  clientOid: str
  errorMsg: str
  errorCode: NotRequired[str]

class BatchPlaceOrderData(TypedDict):
  successList: list[BatchPlaceOrderSuccessItem]
  failureList: list[BatchPlaceOrderFailureItem]

validate_response = validator(BatchPlaceOrderData)

@dataclass
class BatchPlaceOrders(AuthEndpoint):
  @rate_limit(timedelta(seconds=1))
  async def batch_place_orders(
    self,
    symbol: str,
    order_list: list[BatchOrderInput],
    *,
    batch_mode: Literal['single', 'multiple'] | None = None,
    validate: bool | None = None
  ) -> BatchPlaceOrderData:
    """Batch Place Orders

    - `symbol`: Trading pair (used in single mode). e.g. USDCUSDT.
    - `order_list`: List of orders. Each: side, orderType, size, force (for limit), price (optional), clientOid (optional). Returns data with successList and failureList.
    - `batch_mode`: single (default) / multiple.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Batch-Place-Orders)
    """
    json_body: dict = {'symbol': symbol, 'orderList': order_list}
    if batch_mode is not None:
      json_body['batchMode'] = batch_mode
    r = await self.authed_request('POST', '/api/v2/spot/trade/batch-orders', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
