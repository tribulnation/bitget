from typing_extensions import Literal
from datetime import datetime, timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class PlanOrderItem(TypedDict):
  orderId: str
  clientOid: str
  symbol: str
  triggerPrice: Decimal
  orderType: Literal['limit', 'market']
  executePrice: Decimal
  planType: Literal['amount', 'total']
  size: Decimal
  status: str
  side: Literal['buy', 'sell']
  triggerType: Literal['fill_price', 'mark_price']
  enterPointSource: str
  cTime: Timestamp
  uTime: Timestamp

class CurrentPlanOrdersData(TypedDict):
  nextFlag: bool
  idLessThan: str
  orderList: list[PlanOrderItem]

validate_response = validator(CurrentPlanOrdersData)

@dataclass
class CurrentPlanOrders(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def current_plan_orders(self, *, symbol: str | None = None, limit: int | None = None, id_less_than: str | None = None, start: datetime | None = None, end: datetime | None = None, validate: bool | None = None) -> CurrentPlanOrdersData:
    """Get Current Plan Orders. > [Bitget API docs](https://www.bitget.com/api-doc/spot/plan/Get-Current-Plan-Order)"""
    params: dict = {}
    if symbol is not None: params['symbol'] = symbol
    if limit is not None: params['limit'] = limit
    if id_less_than is not None: params['idLessThan'] = id_less_than
    if start is not None: params['startTime'] = ts.dump(start)
    if end is not None: params['endTime'] = ts.dump(end)
    r = await self.authed_request('GET', '/api/v2/spot/trade/current-plan-order', params=params)
    return self.output(r.text, validate_response, validate=validate)
