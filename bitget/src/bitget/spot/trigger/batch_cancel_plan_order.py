from datetime import timedelta
from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class BatchCancelPlanSuccessItem(TypedDict):
  orderId: str
  clientOid: str

class BatchCancelPlanFailureItem(TypedDict):
  orderId: str
  clientOid: str
  errorMsg: str

class BatchCancelPlanOrderData(TypedDict):
  successList: list[BatchCancelPlanSuccessItem] | None  # API may return null when empty
  failureList: list[BatchCancelPlanFailureItem] | None

validate_response = validator(BatchCancelPlanOrderData)

@dataclass
class BatchCancelPlanOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/5))
  async def batch_cancel_plan_order(
    self,
    *,
    symbol_list: list[str] | None = None,
    validate: bool | None = None
  ) -> BatchCancelPlanOrderData:
    """Cancel Plan Orders in Batch

    - `symbol_list`: Trading pairs, e.g. ["USDCUSDT"]. If empty, all spot trigger orders cancelled.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/plan/Batch-Cancel-Plan-Order)
    """
    json_body: dict = {}
    if symbol_list is not None:
      json_body['symbolList'] = symbol_list
    r = await self.authed_request('POST', '/api/v2/spot/trade/batch-cancel-plan-order', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
