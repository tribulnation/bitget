from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime, timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class TransferRecordItem(TypedDict):
  coin: str
  status: str
  toType: str
  toSymbol: str
  fromType: str
  fromSymbol: str
  size: str
  ts: Timestamp
  clientOid: str
  transferId: str

validate_response = validator(list[TransferRecordItem])

AccountType = Literal['spot', 'p2p', 'coin_futures', 'usdt_futures', 'usdc_futures', 'crossed_margin', 'isolated_margin']

@dataclass
class TransferRecords(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def transfer_records(self, coin: str, *, from_type: AccountType | None = None, start: datetime | None = None, end: datetime | None = None, client_oid: str | None = None, limit: int | None = None, id_less_than: str | None = None, validate: bool | None = None) -> list[TransferRecordItem]:
    params = {'coin': coin}
    if from_type is not None:
      params['fromType'] = from_type
    if start is not None:
      params['startTime'] = ts.dump(start)
    if end is not None:
      params['endTime'] = ts.dump(end)
    if client_oid is not None:
      params['clientOid'] = client_oid
    if limit is not None:
      params['limit'] = limit
    if id_less_than is not None:
      params['idLessThan'] = id_less_than
    r = await self.authed_request('GET', '/api/v2/spot/account/transferRecords', params=params)
    return self.output(r.text, validate_response, validate=validate)
