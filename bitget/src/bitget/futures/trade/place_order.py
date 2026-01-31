from typing_extensions import Literal
from dataclasses import dataclass
from bitget.core import AuthEndpoint, validator, TypedDict

class PlaceOrderData(TypedDict):
    orderId: str
    clientOid: str

validate_response = validator(PlaceOrderData)

@dataclass
class PlaceOrder(AuthEndpoint):
    async def place_order(self, product_type, symbol, margin_mode, margin_coin, size, side, order_type, *, price=None, trade_side=None, force=None, client_oid=None, reduce_only=None, validate=None):
        json = {"symbol": symbol, "productType": product_type, "marginMode": margin_mode, "marginCoin": margin_coin, "size": size, "side": side, "orderType": order_type}
        if price is not None: json["price"] = price
        if trade_side is not None: json["tradeSide"] = trade_side
        if force is not None: json["force"] = force
        if client_oid is not None: json["clientOid"] = client_oid
        if reduce_only is not None: json["reduceOnly"] = reduce_only
        r = await self.authed_request("POST", "/api/v2/mix/order/place-order", json=json)
        return self.output(r.text, validate_response, validate=validate)
