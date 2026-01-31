from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class TransferData(TypedDict):
  transferId: str
  clientOid: str

validate_response = validator(TransferData)

@dataclass
class Transfer(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def transfer(self, from_type: str, to_type: str, amount: str, coin: str, *, symbol: str | None = None, client_oid: str | None = None, validate: bool | None = None) -> TransferData:
    json_body = {"fromType": from_type, "toType": to_type, "amount": amount, "coin": coin}
    if symbol is not None:
      json_body["symbol"] = symbol
    if client_oid is not None:
      json_body["clientOid"] = client_oid
    r = await self.authed_request("POST", "/api/v2/spot/wallet/transfer", json=json_body)
    return self.output(r.text, validate_response, validate=validate)
