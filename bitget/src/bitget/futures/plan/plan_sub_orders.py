from typing_extensions import Literal
from dataclasses import dataclass
from bitget.core import AuthEndpoint, validator, TypedDict

class PlanSubOrderItem(TypedDict):
    orderId: str
    price: str
    type: Literal["limit", "market"]
    status: str

validate_response = validator(list[PlanSubOrderItem])

@dataclass
class PlanSubOrders(AuthEndpoint):
    async def plan_sub_orders(self, product_type, plan_type, plan_order_id, *, validate=None):
        params = {"productType": product_type, "planType": plan_type, "planOrderId": plan_order_id}
        r = await self.authed_request("GET", "/api/v2/mix/order/plan-sub-order", params=params)
        return self.output(r.text, validate_response, validate=validate)
