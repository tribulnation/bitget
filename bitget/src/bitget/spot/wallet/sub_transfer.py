from datetime import timedelta
from dataclasses import dataclass

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class SubTransferData(TypedDict):
  transferId: str
  clientOid: str

validate_response = validator(SubTransferData)

@dataclass
class SubTransfer(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def sub_transfer(self, from_type: str, to_type: str, amount: str, coin: str, from_user_id: str, to_user_id: str, *, symbol: str | None = None, client_oid: str | None = None, validate: bool | None = None) -> SubTransferData:
    """Sub Transfer. from_type/to_type: spot, p2p, coin_futures, usdt_futures, usdc_futures, crossed_margin, isolated_margin. > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Sub-Transfer)"""
    json_body: dict = {'fromType': from_type, 'toType': to_type, 'amount': amount, 'coin': coin, 'fromUserId': from_user_id, 'toUserId': to_user_id}
    if symbol is not None: json_body['symbol'] = symbol
    if client_oid is not None: json_body['clientOid'] = client_oid
    r = await self.authed_request('POST', '/api/v2/spot/wallet/subaccount-transfer', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
