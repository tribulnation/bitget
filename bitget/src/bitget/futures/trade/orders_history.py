"""Get history orders. Auth required."""
from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime

from bitget.core import AuthEndpoint, validator, TypedDict, timestamp as ts, Timestamp

class HistoryOrderItem(TypedDict):
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

class OrdersHistoryResponse(TypedDict):
    entrustedList: list[HistoryOrderItem]
    endId: str

validate_response = validator(OrdersHistoryResponse)

@dataclass
class OrdersHistory(AuthEndpoint):
    async def orders_history(
        self,
        product_type: Literal["USDT-FUTURES", "COIN-FUTURES", "USDC-FUTURES"],
        *,
        symbol: str | None = None,
        order_id: str | None = None,
        client_oid: str | None = None,
        order_source: str | None = None,
        id_less_than: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None,
        validate: bool | None = None
    ):
        """Get history orders (data within 90 days). Use symbol=USDCUSDT to filter."""
        params = {'productType': product_type}
        if symbol is not None:
            params['symbol'] = symbol
        if order_id is not None:
            params['orderId'] = order_id
        if client_oid is not None:
            params['clientOid'] = client_oid
        if order_source is not None:
            params['orderSource'] = order_source
        if id_less_than is not None:
            params['idLessThan'] = id_less_than
        if start is not None:
            params['startTime'] = ts.dump(start)
        if end is not None:
            params['endTime'] = ts.dump(end)
        if limit is not None:
            params['limit'] = str(limit)
        r = await self.authed_request('GET', '/api/v2/mix/order/orders-history', params=params)
        return self.output(r.text, validate_response, validate=validate)
