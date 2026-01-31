from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp
from datetime import timedelta

class AccountInfoData(TypedDict):
  userId: str
  inviterId: str
  channelCode: str
  channel: str
  ips: str | None
  authorities: list[str]
  parentId: int
  traderType: str
  regisTime: Timestamp

validate_response = validator(AccountInfoData)

@dataclass
class AccountInfo(AuthEndpoint):
  @rate_limit(timedelta(seconds=1))
  async def account_info(self, *, validate: bool | None = None) -> AccountInfoData:
    """Get Account Information

    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Get-Account-Info)
    """
    r = await self.authed_request('GET', '/api/v2/spot/account/info')
    return self.output(r.text, validate_response, validate=validate)
