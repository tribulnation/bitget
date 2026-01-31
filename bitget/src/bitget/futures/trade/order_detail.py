from typing_extensions import Literal
from dataclasses import dataclass
from bitget.core import AuthEndpoint, validator, TypedDict, Timestamp

class OrderDetail(TypedDict):
    symbol: str
    size: str
    orderId: str
    clientOid: str
    baseVolume: str
    priceAvg: str
    fee: str
    price: str
    state: str
    side: Literal["buy", "sell"]
    force: str
    totalProfits: str
    posSide: str
    marginCoin: str
    quoteVolume: str
    orderType: Literal["limit", "market"]
    leverage: str
    marginMode: str
    reduceOnly: str
    enterPointSource: str
    tradeSide: str
    posMode: Literal["one_way_mode", "hedge_mode"]
    orderSource: str
    cancelReason: str
    cTime: Timestamp
    uTime: Timestamp

validate_response = validator(OrderDetail)

@dataclass
class OrderDetailEndpoint(AuthEndpoint):
    async def order_detail(self, product_type, symbol, *, order_id=None, client_oid=None, validate=None):
        params = {"productType": product_type, "symbol": symbol}
        if order_id is not None:
            params["orderId"] = order_id
        if client_oid is not None:
            params["clientOid"] = client_oid
        r = await self.authed_request("GET", "/api/v2/mix/order/detail", params=params)
        return self.output(r.text, validate_response, validate=validate)
