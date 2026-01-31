from typing_extensions import Literal
from datetime import timedelta
from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class PlacePlanOrderData(TypedDict):
  orderId: str
  clientOid: str

validate_response = validator(PlacePlanOrderData)

@dataclass
class PlacePlanOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def place_plan_order(
    self,
    symbol: str,
    side: Literal['buy', 'sell'],
    trigger_price: str,
    order_type: Literal['limit', 'market'],
    size: str,
    trigger_type: Literal['fill_price', 'mark_price'],
    *,
    execute_price: str | None = None,
    plan_type: Literal['amount', 'total'] | None = None,
    client_oid: str | None = None,
    validate: bool | None = None
  ) -> PlacePlanOrderData:
    """Place Plan Order. > [Bitget API docs](https://www.bitget.com/api-doc/spot/plan/Place-Plan-Order)"""
    json_body: dict = {'symbol': symbol, 'side': side, 'triggerPrice': trigger_price, 'orderType': order_type, 'size': size, 'triggerType': trigger_type}
    if execute_price is not None: json_body['executePrice'] = execute_price
    if plan_type is not None: json_body['planType'] = plan_type
    if client_oid is not None: json_body['clientOid'] = client_oid
    r = await self.authed_request('POST', '/api/v2/spot/trade/place-plan-order', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
