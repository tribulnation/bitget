"""Get single-symbol ticker. Public endpoint."""
from typing_extensions import Literal
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, validator, TypedDict

class TickerItem(TypedDict):
    symbol: str
    """Trading pair name"""
    lastPr: Decimal
    """Last price"""
    askPr: Decimal
    """Ask price"""
    bidPr: Decimal
    """Bid price"""
    bidSz: Decimal
    """Buying amount"""
    askSz: Decimal
    """Selling amount"""
    high24h: Decimal
    """24h high"""
    low24h: Decimal
    """24h low"""
    ts: int
    """Current data timestamp, ms"""
    change24h: Decimal
    """Price change (24h)"""
    baseVolume: Decimal
    """Trading volume (base)"""
    quoteVolume: Decimal
    """Trading volume (quote)"""
    usdtVolume: Decimal
    """Trading volume (USDT)"""
    openUtc: Decimal
    """UTC0 opening price"""
    changeUtc24h: Decimal
    """UTC0 24h price change"""
    indexPrice: Decimal
    """Index price"""
    fundingRate: Decimal
    """Funding rate"""
    holdingAmount: Decimal
    """Current positions (base coin)"""
    open24h: Decimal
    """Entry price last 24h"""
    markPrice: Decimal
    """Mark price"""

validate_response = validator(list[TickerItem])

@dataclass
class Ticker(Endpoint):
    async def ticker(
        self,
        product_type: Literal['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES'],
        symbol: str,
        *,
        validate: bool | None = None
    ):
        """Get ticker for a single symbol (e.g. USDCUSDT).

        - `product_type`: Product type.
        - `symbol`: Trading pair, e.g. USDCUSDT.
        - `validate`: Whether to validate the response (default: True).

        > [Bitget API docs](https://www.bitget.com/api-doc/contract/market/Get-Ticker)
        """
        r = await self.request('GET', '/api/v2/mix/market/ticker', params={
            'productType': product_type,
            'symbol': symbol,
        })
        return self.output(r.text, validate_response, validate=validate)
