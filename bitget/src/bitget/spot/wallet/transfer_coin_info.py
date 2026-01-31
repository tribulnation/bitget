from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator

validate_response = validator(list[str])

@dataclass
class TransferCoinInfo(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def transfer_coin_info(self, from_type: str, to_type: str, *, validate: bool | None = None) -> list[str]:
    params = {"fromType": from_type, "toType": to_type}
    r = await self.authed_request("GET", "/api/v2/spot/wallet/transfer-coin-info", params=params)
    return self.output(r.text, validate_response, validate=validate)
