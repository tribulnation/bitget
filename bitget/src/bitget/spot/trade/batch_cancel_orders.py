from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class BatchCancelSuccessItem(TypedDict):
  orderId: str
  clientOid: str

class BatchCancelFailureItem(TypedDict):
  orderId: str
  clientOid: str
  errorMsg: str

class BatchCancelOrdersData(TypedDict):
  successList: list[BatchCancelSuccessItem]
  failureList: list[BatchCancelFailureItem]

validate_response = validator(BatchCancelOrdersData)

@dataclass
class BatchCancelOrders(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def batch_cancel_orders(
    self,
    order_list: list[dict],
    *,
    symbol: str | None = None,
    batch_mode: str | None = None,
    validate: bool | None = None
  ) -> BatchCancelOrdersData:
    """Batch Cancel Orders

    - `order_list`: List of {orderId} or {clientOid}. Do not mix.
    - `symbol`: Trading pair (single mode).
    - `batch_mode`: single (default) / multiple.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Batch-Cancel-Orders)
    """
    json_body: dict = {'orderList': order_list}
    if symbol is not None:
      json_body['symbol'] = symbol
    if batch_mode is not None:
      json_body['batchMode'] = batch_mode
    r = await self.authed_request('POST', '/api/v2/spot/trade/batch-cancel-order', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
