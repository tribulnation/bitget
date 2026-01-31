from typing_extensions import Literal
from datetime import timedelta
from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class ModifyPlanOrderData(TypedDict):
  orderId: str
  clientOid: str

validate_response = validator(ModifyPlanOrderData)

@dataclass
class ModifyPlanOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def modify_plan_order(
    self,
    trigger_price: str,
    order_type: Literal['limit', 'market'],
    size: str,
    *,
    order_id: str | None = None,
    client_oid: str | None = None,
    execute_price: str | None = None,
    validate: bool | None = None
  ) -> ModifyPlanOrderData:
    """Modify Plan Order

    Either order_id or client_oid is required.

    - `trigger_price`: Trigger price.
    - `order_type`: limit / market.
    - `size`: Quantity.
    - `order_id`: Order ID.
    - `client_oid`: Client order ID.
    - `execute_price`: Required when order_type=limit.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/plan/Modify-Plan-Order)
    """
    json_body: dict = {'triggerPrice': trigger_price, 'orderType': order_type, 'size': size}
    if order_id is not None:
      json_body['orderId'] = order_id
    if client_oid is not None:
      json_body['clientOid'] = client_oid
    if execute_price is not None:
      json_body['executePrice'] = execute_price
    r = await self.authed_request('POST', '/api/v2/spot/trade/modify-plan-order', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
