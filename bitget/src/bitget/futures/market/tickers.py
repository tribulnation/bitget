"""Get all tickers. Public endpoint."""
from typing_extensions import Literal
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, validator, TypedDict

class TickerItem(TypedDict):
    symbol: str
    lastPr: Decimal
    askPr: Decimal
    bidPr: Decimal
    bidSz: Decimal
    askSz: Decimal
    high24h: Decimal
    low24h: Decimal
    ts: int
    change24h: Decimal
    baseVolume: Decimal
    quoteVolume: Decimal
    usdtVolume: Decimal
    openUtc: Decimal
    changeUtc24h: Decimal
    indexPrice: Decimal
    fundingRate: Decimal
    holdingAmount: Decimal
    open24h: Decimal
    markPrice: Decimal

validate_response = validator(list[TickerItem])

@dataclass
class Tickers(Endpoint):
    async def tickers(
        self,
        product_type: Literal['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES'],
        *,
        validate: bool | None = None
    ):
        """Get all tickers for a product type.

        - `product_type`: Product type.
        - `validate`: Whether to validate the response (default: True).

        > [Bitget API docs](https://www.bitget.com/api-doc/contract/market/Get-All-Symbol-Ticker)
        """
        r = await self.request('GET', '/api/v2/mix/market/tickers', params={'productType': product_type})
        return self.output(r.text, validate_response, validate=validate)
