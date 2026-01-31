# STDLIB IMPORTS
from dataclasses import dataclass
from datetime import timedelta

from bitget.core import (
  AuthEndpoint, rate_limit,
  validator, TypedDict
)

# RESPONSE MODELS

class DepositAddressData(TypedDict):
  address: str
  """Deposit address"""
  chain: str
  """Chain name"""
  coin: str
  """Token name"""
  tag: str | None
  """Tag (optional; null when not used)"""
  url: str | None
  """Blockchain address (optional)"""

validate_response = validator(DepositAddressData)

# ENDPOINT CLASS

@dataclass
class DepositAddress(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def deposit_address(
    self,
    coin: str,
    *,
    chain: str | None = None,
    size: str | None = None,
    validate: bool | None = None
  ):
    """Get Deposit Address

    - `coin`: Coin name, e.g. USDT. All coin names can be returned from Get Coin Info.
    - `chain`: Chain name, e.g. trc20. You can get the chain names via Get Coin Info.
    - `size`: Bitcoin Lightning Network withdrawal amount, limit: 0.000001 - 0.01
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Get-Deposit-Address)
    """
    params = {}
    params['coin'] = coin
    if chain is not None:
      params['chain'] = chain
    if size is not None:
      params['size'] = size

    r = await self.authed_request('GET', '/api/v2/spot/wallet/deposit-address', params=params)
    return self.output(r.text, validate_response, validate=validate)
