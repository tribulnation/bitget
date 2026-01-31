from datetime import timedelta
from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class SubaccountDepositAddressData(TypedDict):
  address: str
  chain: str
  coin: str
  tag: str | None
  url: str | None

validate_response = validator(SubaccountDepositAddressData)

@dataclass
class SubaccountDepositAddress(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/10))
  async def subaccount_deposit_address(self, sub_uid: str, coin: str, *, chain: str | None = None, size: str | None = None, validate: bool | None = None) -> SubaccountDepositAddressData:
    """Get Sub-account Deposit Address. > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Get-SubAccount-Deposit-Address)"""
    params: dict = {'subUid': sub_uid, 'coin': coin}
    if chain is not None: params['chain'] = chain
    if size is not None: params['size'] = size
    r = await self.authed_request('GET', '/api/v2/spot/wallet/subaccount-deposit-address', params=params)
    return self.output(r.text, validate_response, validate=validate)
