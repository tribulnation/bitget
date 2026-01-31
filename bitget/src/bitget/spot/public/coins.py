# STDLIB IMPORTS
from typing_extensions import Literal
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict

# RESPONSE MODELS (nested first, then main)

class CoinChain(TypedDict):
  chain: str
  """Chain name"""
  needTag: bool
  """Need tag"""
  withdrawable: bool
  """Withdrawal supported"""
  rechargeable: bool
  """Deposit supported"""
  withdrawFee: Decimal
  """Withdrawal transaction fee"""
  extraWithdrawFee: Decimal
  """Extra charge. On chain destruction: 0.1 means 10%"""
  depositConfirm: int
  """Deposit confirmation blocks"""
  withdrawConfirm: int
  """Withdrawal confirmation blocks"""
  minDepositAmount: Decimal
  """Minimum deposit amount"""
  minWithdrawAmount: Decimal
  """Minimum withdrawal amount"""
  browserUrl: str | None
  """Blockchain explorer address"""
  contractAddress: str | None
  """Coin contract address (null for native chain)"""
  withdrawStep: Decimal
  """Withdrawal count step. If not 0, withdrawal size should be multiple of this value"""
  withdrawMinScale: int
  """Decimal places of withdrawal amount"""
  congestion: Literal['normal', 'congested']
  """Chain network status: normal, congested"""

class CoinInfo(TypedDict):
  coinId: str
  """Currency ID"""
  coin: str
  """Token name"""
  transfer: str
  """Transferability"""
  chains: list[CoinChain]
  """Support chain list"""

validate_response = validator(list[CoinInfo])

# ENDPOINT CLASS

@dataclass
class Coins(Endpoint):
  @rate_limit(timedelta(seconds=1/3))
  async def coins(
    self,
    *,
    coin: str | None = None,
    validate: bool | None = None
  ):
    """Get Coin Info

    Get spot coin information, supporting both individual and full queries.

    - `coin`: Coin name. If blank, all coin information is returned.
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-Coin-List)
    """
    params = {}
    if coin is not None:
      params['coin'] = coin
    r = await self.request('GET', '/api/v2/spot/public/coins', params=params)
    return self.output(r.text, validate_response, validate=validate)
