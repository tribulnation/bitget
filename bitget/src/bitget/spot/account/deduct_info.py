from typing_extensions import Literal
from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class DeductInfoData(TypedDict):
  deduct: Literal['on', 'off']

validate_response = validator(DeductInfoData)

@dataclass
class DeductInfo(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/5))
  async def deduct_info(
    self,
    *,
    validate: bool | None = None
  ) -> DeductInfoData:
    """Get BGB Deduct Info

    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Get-Deduct-Info)
    """
    r = await self.authed_request('GET', '/api/v2/spot/account/deduct-info')
    return self.output(r.text, validate_response, validate=validate)
