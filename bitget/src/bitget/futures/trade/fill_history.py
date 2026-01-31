# Get fill history. Auth required. Max 1 week range.
from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime
from bitget.core import AuthEndpoint, validator, timestamp as ts
from .fills import FillsResponse

validate_response = validator(FillsResponse)

@dataclass
class FillHistory(AuthEndpoint):
    async def fill_history(self, product_type, *, symbol=None, order_id=None, client_oid=None, id_less_than=None, start=None, end=None, limit=None, validate=None):
        """Get historical transaction details. Max time span 1 week. Use symbol=USDCUSDT to filter."""
        params = {"productType": product_type}
        if symbol is not None: params["symbol"] = symbol
        if order_id is not None: params["orderId"] = order_id
        if client_oid is not None: params["clientOid"] = client_oid
        if id_less_than is not None: params["idLessThan"] = id_less_than
        if start is not None: params["startTime"] = ts.dump(start)
        if end is not None: params["endTime"] = ts.dump(end)
        if limit is not None: params["limit"] = str(limit)
        r = await self.authed_request("GET", "/api/v2/mix/order/fill-history", params=params)
        return self.output(r.text, validate_response, validate=validate)
