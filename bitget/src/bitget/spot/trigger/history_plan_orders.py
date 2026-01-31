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

class HistoryPlanOrdersData(TypedDict):
  nextFlag: bool
  idLessThan: str
  orderList: list[PlanOrderItem]

validate_response = validator(HistoryPlanOrdersData)

@dataclass
class HistoryPlanOrders(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def history_plan_orders(self, *, symbol: str | None = None, start: datetime | None = None, end: datetime | None = None, limit: int | None = None, id_less_than: str | None = None, validate: bool | None = None) -> HistoryPlanOrdersData:
    """Get History Plan Orders. > [Bitget API docs](https://www.bitget.com/api-doc/spot/plan/Get-History-Plan-Order)"""
    params: dict = {}
    if symbol is not None: params['symbol'] = symbol
    if start is not None: params['startTime'] = ts.dump(start)
    if end is not None: params['endTime'] = ts.dump(end)
    if limit is not None: params['limit'] = limit
    if id_less_than is not None: params['idLessThan'] = id_less_than
    r = await self.authed_request('GET', '/api/v2/spot/trade/history-plan-order', params=params)
    return self.output(r.text, validate_response, validate=validate)
