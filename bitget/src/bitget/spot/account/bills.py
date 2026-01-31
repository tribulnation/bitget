from datetime import datetime, timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class BillItem(TypedDict):
  cTime: Timestamp
  coin: str
  groupType: str
  businessType: str
  size: Decimal
  balance: Decimal
  fees: Decimal
  billId: str

validate_response = validator(list[BillItem])

@dataclass
class Bills(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/10))
  async def bills(
    self,
    *,
    coin: str | None = None,
    group_type: str | None = None,
    business_type: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    id_less_than: str | None = None,
    validate: bool | None = None
  ) -> list[BillItem]:
    """Get Account Bills

    - `coin`: Token name, e.g. USDT.
    - `group_type`: deposit, withdraw, transaction, transfer, loan, financial, fiat, convert, c2c, etc.
    - `business_type`: DEPOSIT, WITHDRAW, BUY, SELL, etc.
    - `start`, `end`: Time range (max 90 days).
    - `limit`: Default 100, max 500.
    - `id_less_than`: Pagination, billId.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Get-Account-Bills)
    """
    params: dict = {}
    if coin is not None:
      params['coin'] = coin
    if group_type is not None:
      params['groupType'] = group_type
    if business_type is not None:
      params['businessType'] = business_type
    if start is not None:
      params['startTime'] = ts.dump(start)
    if end is not None:
      params['endTime'] = ts.dump(end)
    if limit is not None:
      params['limit'] = limit
    if id_less_than is not None:
      params['idLessThan'] = id_less_than
    r = await self.authed_request('GET', '/api/v2/spot/account/bills', params=params)
    return self.output(r.text, validate_response, validate=validate)
