from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class BatchCancelReplaceItemResult(TypedDict):
  orderId: str
  clientOid: str
  success: str
  msg: str

validate_response = validator(list[BatchCancelReplaceItemResult])

@dataclass
class BatchCancelReplaceOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/5))
  async def batch_cancel_replace_order(self, order_list: list, *, validate: bool | None = None) -> list[BatchCancelReplaceItemResult]:
    r = await self.authed_request("POST", "/api/v2/spot/trade/batch-cancel-replace-order", json={"orderList": order_list})
    return self.output(r.text, validate_response, validate=validate)
