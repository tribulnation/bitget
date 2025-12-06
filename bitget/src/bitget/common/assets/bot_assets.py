from typing_extensions import Literal
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import AuthEndpoint, validator, TypedDict

AccountType = Literal['spot', 'futures']

class Asset(TypedDict):
  coin: str
  available: Decimal
  equity: Decimal
  """Total account equity"""
  bonus: Decimal
  frozen: Decimal
  usdtValue: Decimal


validate_response = validator(list[Asset])

@dataclass
class BotAssets(AuthEndpoint):
  async def bot_assets(self, account_type: AccountType | None = None, *, validate: bool | None = None):
    """Bot assets
    
    - `account_type`: Filter by account type, e.g. spot, futures.
    - `validate`: Whether to validate the response against the expected schema (default: True).
    
    > [Bitget API docs](https://www.bitget.com/api-doc/common/account/Bot-Assets)
    """
    params = {}
    if account_type is not None:
      params['accountType'] = account_type
    r = await self.authed_request('GET', '/api/v2/account/bot-assets', params=params)
    return self.output(r.text, validate_response, validate=validate)