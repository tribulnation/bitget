from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class WithdrawalData(TypedDict):
  orderId: str
  clientOid: str

validate_response = validator(WithdrawalData)

@dataclass
class Withdrawal(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/5))
  async def withdrawal(self, coin: str, transfer_type: str, address: str, size: str, *, chain: str | None = None, inner_to_type: str | None = None, area_code: str | None = None, tag: str | None = None, remark: str | None = None, client_oid: str | None = None, validate: bool | None = None) -> WithdrawalData:
    json_body = {'coin': coin, 'transferType': transfer_type, 'address': address, 'size': size}
    if chain is not None:
      json_body['chain'] = chain
    if inner_to_type is not None:
      json_body['innerToType'] = inner_to_type
    if area_code is not None:
      json_body['areaCode'] = area_code
    if tag is not None:
      json_body['tag'] = tag
    if remark is not None:
      json_body['remark'] = remark
    if client_oid is not None:
      json_body['clientOid'] = client_oid
    r = await self.authed_request('POST', '/api/v2/spot/wallet/withdrawal', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
