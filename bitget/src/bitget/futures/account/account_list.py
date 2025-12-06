from typing_extensions import Literal
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import AuthEndpoint, validator, TypedDict
from bitget.futures.core import ProductType

class AccountAsset(TypedDict):
  coin: str
  """Coin name"""
  balance: Decimal
  """Balance"""
  available: Decimal
  """Maximum transferable amount"""

class Account(TypedDict):
    marginCoin: str
    """Margin coin"""
    locked: Decimal
    """Locked quantity (margin coin)"""
    available: Decimal
    """Available quantity in the account (margin coin)"""
    crossedMaxAvailable: Decimal
    """Maximum available balance to open positions under the cross margin mode (margin coin)"""
    isolatedMaxAvailable: Decimal
    """Maximum available balance to open positions under the isolated margin mode (margin coin)"""
    maxTransferOut: Decimal
    """Maximum transferable amount"""
    accountEquity: Decimal
    """Account equity (margin coin). Includes unrealized PnL (based on mark price)"""
    usdtEquity: Decimal
    """Account equity in USDT"""
    btcEquity: Decimal
    """Account equity in BTC"""
    crossedRiskRate: Decimal
    """Risk ratio in cross margin mode"""
    unrealizedPL: Decimal
    """Unrealized PnL"""
    coupon: Decimal
    """Trading bonus"""
    unionTotalMargin: Decimal
    """Multi-assets multi-assets mode"""
    unionAvailable: Decimal
    """Available under multi-assets mode"""
    unionMm: Decimal
    """Maintenance margin under multi-assets mode"""
    assetList: list[AccountAsset]
    """Assets list under multi-assets mode"""
    isolatedMargin: Decimal
    """Isolated Margin Occupied"""
    crossedMargin: Decimal
    """Crossed Margin Occupied"""
    crossedUnrealizedPL: Decimal
    """unrealizedPL for crossed"""
    isolatedUnrealizedPL: Decimal
    """unrealizedPL for isolated"""
    assetMode: Literal['union', 'single']
    """Assets mode. `union` Multi-assets mode, `single` Single-assets mode"""


validate_response = validator(list[Account])

@dataclass
class AccountList(AuthEndpoint):
  async def account_list(
    self, product_type: ProductType, *,
    validate: bool | None = None
  ):
    """Query all account information under a certain product type.
    
    - `product_type`: Product type.
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/contract/account/Get-Account-List)
    """
    r = await self.authed_request('GET', '/api/v2/mix/account/accounts', params={
      'productType': product_type,
    })
    return self.output(r.text, validate_response, validate=validate)