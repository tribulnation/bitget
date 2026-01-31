"""Get single account (by symbol + marginCoin). Auth required."""
from typing_extensions import Literal, NotRequired
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import AuthEndpoint, validator, TypedDict

class SingleAccount(TypedDict):
    marginCoin: str
    locked: Decimal
    available: Decimal
    crossedMaxAvailable: Decimal
    isolatedMaxAvailable: Decimal
    maxTransferOut: Decimal
    accountEquity: Decimal
    usdtEquity: Decimal
    btcEquity: Decimal
    crossedRiskRate: Decimal
    crossedMarginLeverage: NotRequired[Decimal]
    isolatedLongLever: NotRequired[Decimal]
    isolatedShortLever: NotRequired[Decimal]
    marginMode: Literal['isolated', 'crossed']
    posMode: Literal['one_way_mode', 'hedge_mode']
    unrealizedPL: Decimal
    coupon: Decimal
    crossedUnrealizedPL: Decimal | Literal['']
    isolatedUnrealizedPL: Decimal | Literal['']
    grant: Decimal
    assetMode: Literal['union', 'single']
    isolatedMargin: Decimal | None
    crossedMargin: Decimal | None

validate_response = validator(SingleAccount)

@dataclass
class SingleAccountEndpoint(AuthEndpoint):
    async def single_account(
        self,
        product_type: Literal['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES'],
        symbol: str,
        margin_coin: str,
        *,
        validate: bool | None = None
    ):
        """Get account details for a given symbol and margin coin (e.g. USDCUSDT, USDT).

        - `product_type`: Product type.
        - `symbol`: Trading pair, e.g. USDCUSDT.
        - `margin_coin`: Margin coin, e.g. USDT.
        - `validate`: Whether to validate the response (default: True).

        > [Bitget API docs](https://www.bitget.com/api-doc/contract/account/Get-Single-Account)
        """
        r = await self.authed_request('GET', '/api/v2/mix/account/account', params={
            'productType': product_type,
            'symbol': symbol,
            'marginCoin': margin_coin,
        })
        return self.output(r.text, validate_response, validate=validate)
