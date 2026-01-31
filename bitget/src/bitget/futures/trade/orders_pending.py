from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime
from bitget.core import AuthEndpoint, validator, TypedDict, timestamp as ts, Timestamp

class PendingOrderItem(TypedDict):
    symbol: str
    size: str
    orderId: str
    clientOid: str
    baseVolume: str
    fee: str
    price: str
    priceAvg: str
    status: str
    side: str
    force: str
    totalProfits: str
    posSide: str
    marginCoin: str
    quoteVolume: str
    leverage: str
    marginMode: str
    enterPointSource: str
    tradeSide: str
    posMode: str
    orderType: str
    orderSource: str
    cTime: Timestamp
    uTime: Timestamp

class OrdersPendingResponse(TypedDict):
    entrustedList: list[PendingOrderItem]
    endId: str

validate_response = validator(OrdersPendingResponse)

@dataclass
class OrdersPending(AuthEndpoint):
    async def orders_pending(self, product_type, *, symbol=None, order_id=None, client_oid=None, status=None, id_less_than=None, start=None, end=None, limit=None, validate=None):
        params = {"productType": product_type}
        if symbol is not None:
            params["symbol"] = symbol
        if order_id is not None:
            params["orderId"] = order_id
        if client_oid is not None:
            params["clientOid"] = client_oid
        if status is not None:
            params["status"] = status
        if id_less_than is not None:
            params["idLessThan"] = id_less_than
        if start is not None:
            params["startTime"] = ts.dump(start)
        if end is not None:
            params["endTime"] = ts.dump(end)
        if limit is not None:
            params["limit"] = str(limit)
        r = await self.authed_request("GET", "/api/v2/mix/order/orders-pending", params=params)
        return self.output(r.text, validate_response, validate=validate)
