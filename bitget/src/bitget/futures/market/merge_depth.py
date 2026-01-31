"""Get merge market depth. Public endpoint."""
from typing_extensions import Literal
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, validator, TypedDict, Timestamp

class MergeDepthData(TypedDict):
    asks: list[list[Decimal]]
    """Selling price [price, quantity]"""
    bids: list[list[Decimal]]
    """Buying price [price, quantity]"""
    ts: Timestamp
    """Matching engine timestamp, ms"""
    scale: str
    """Actual precision value"""
    precision: str
    """Requested precision (scale0/scale1/scale2/scale3)"""
    isMaxPrecision: str
    """YES/NO"""

validate_response = validator(MergeDepthData)

@dataclass
class MergeDepth(Endpoint):
    async def merge_depth(
        self,
        product_type: Literal['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES'],
        symbol: str,
        *,
        precision: Literal['scale0', 'scale1', 'scale2', 'scale3'] | None = None,
        limit: Literal['1', '5', '15', '50', 'max'] | None = None,
        validate: bool | None = None
    ):
        """Get merge depth (e.g. for USDCUSDT).

        - `product_type`: Product type.
        - `symbol`: Trading pair, e.g. USDCUSDT.
        - `precision`: scale0 (default, no merge) / scale1 / scale2 / scale3.
        - `limit`: 1 / 5 / 15 / 50 / max. Default 100.
        - `validate`: Whether to validate the response (default: True).

        > [Bitget API docs](https://www.bitget.com/api-doc/contract/market/Get-Merge-Depth)
        """
        params = {'productType': product_type, 'symbol': symbol}
        if precision is not None:
            params['precision'] = precision
        if limit is not None:
            params['limit'] = limit
        r = await self.request('GET', '/api/v2/mix/market/merge-depth', params=params)
        return self.output(r.text, validate_response, validate=validate)
