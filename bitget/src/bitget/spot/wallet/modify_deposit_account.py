from datetime import timedelta
from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class ModifyDepositAccountData(TypedDict):
  data: str

validate_response = validator(ModifyDepositAccountData)

@dataclass
class ModifyDepositAccount(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/10))
  async def modify_deposit_account(self, coin: str, account_type: str, *, validate: bool | None = None) -> ModifyDepositAccountData:
    """Modify the auto-transfer account type of deposit. account_type: spot, funding, coin-futures, usdt-futures, usdc-futures. > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Modify-Deposit-Account)"""
    r = await self.authed_request('POST', '/api/v2/spot/wallet/modify-deposit-account', json={'coin': coin, 'accountType': account_type})
    return self.output(r.text, validate_response, validate=validate)
