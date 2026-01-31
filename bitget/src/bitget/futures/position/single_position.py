"""Get single position (one symbol). Auth required."""
from typing_extensions import Literal
from dataclasses import dataclass

from bitget.core import AuthEndpoint, validator
from .all_positions import Position

validate_response = validator(list[Position])

@dataclass
class SinglePosition(AuthEndpoint):
    async def single_position(
        self,
        product_type: Literal['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES'],
        symbol: str,
        margin_coin: str,
        *,
        validate: bool | None = None
    ):
        """Get position for a single symbol (e.g. USDCUSDT).

        - `product_type`: Product type.
        - `symbol`: Trading pair, e.g. USDCUSDT.
        - `margin_coin`: Margin coin, e.g. USDT.
        - `validate`: Whether to validate the response (default: True).

        > [Bitget API docs](https://www.bitget.com/api-doc/contract/position/get-single-position)
        """
        r = await self.authed_request('GET', '/api/v2/mix/position/single-position', params={
            'productType': product_type,
            'symbol': symbol,
            'marginCoin': margin_coin,
        })
        return self.output(r.text, validate_response, validate=validate)
