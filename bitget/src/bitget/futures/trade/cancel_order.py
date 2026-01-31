"""Cancel order. Stick to USDCUSDT only for trading (per project convention)."""
from typing_extensions import Literal
from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, validator, TypedDict, rate_limit

class CancelOrderData(TypedDict):
    orderId: str
    clientOid: str

validate_response = validator(CancelOrderData)

@dataclass
class CancelOrder(AuthEndpoint):
    @rate_limit(timedelta(seconds=0.1))
    async def cancel_order(
        self,
        product_type: Literal["USDT-FUTURES", "COIN-FUTURES", "USDC-FUTURES"],
        symbol: str,
        *,
        order_id: str | None = None,
        client_oid: str | None = None,
        margin_coin: str | None = None,
        validate: bool | None = None
    ):
        """Cancel a pending order. Use symbol=USDCUSDT only (per project convention). Either order_id or client_oid required."""
        json = {"symbol": symbol, "productType": product_type}
        if order_id is not None:
            json["orderId"] = order_id
        if client_oid is not None:
            json["clientOid"] = client_oid
        if margin_coin is not None:
            json["marginCoin"] = margin_coin
        r = await self.authed_request("POST", "/api/v2/mix/order/cancel-order", json=json)
        return self.output(r.text, validate_response, validate=validate)
