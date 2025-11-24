from dataclasses import dataclass
from decimal import Decimal

from bitget.core import ApiAuthMixin, response_validator, TypedDict

class Asset(TypedDict):
  coin: str
  """Token name."""
  symbol: str
  """Trading pair name."""
  totalAmount: Decimal
  """Total amount."""
  available: Decimal
  """Available amount."""
  frozen: Decimal
  """Assets frozen."""
  borrow: Decimal
  """Borrow."""
  interest: Decimal
  """Interest, Interest-only payments with a minimum payment of interest."""
  net: Decimal
  """Net assets = available + frozen - borrow - interest. Liquidation is triggered when the risk ratio is reached 1."""
  coupon: Decimal
  """Trading bonus."""
  cTime: int
  """Creation time."""
  uTime: int
  """Update time."""

validate_response = response_validator(list[Asset])

@dataclass
class AccountAssets(ApiAuthMixin):
  async def account_assets(
    self, *, symbol: str | None = None,
    validate: bool | None = None
  ):
    """Get isolated margin account assets.
    
    - `symbol`: Symbol, e.g. BTCUSDT. This field is used for querying the balance of a single symbol.
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/margin/isolated/account/Get-Isolated-Assets)
    """
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.authed_request('GET', '/api/v2/margin/isolated/account/assets', params=params)
    return self.output(r.text, validate_response, validate=validate)