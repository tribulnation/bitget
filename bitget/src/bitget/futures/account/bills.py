"""Get account bills. Auth required."""
from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from bitget.core import AuthEndpoint, validator, TypedDict, timestamp as ts

class BillItem(TypedDict):
    billId: str
    symbol: str
    amount: Decimal
    fee: Decimal
    feeByCoupon: str
    businessType: str
    coin: str
    balance: Decimal
    cTime: int

class BillsResponse(TypedDict):
    bills: list[BillItem]
    endId: str

validate_response = validator(BillsResponse)

@dataclass
class Bills(AuthEndpoint):
    async def bills(
        self,
        product_type: Literal['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES'],
        *,
        coin: str | None = None,
        business_type: str | None = None,
        only_funding: Literal['yes', 'no'] | None = None,
        id_less_than: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None,
        validate: bool | None = None
    ):
        """Get account bills (data within 90 days).

        - `product_type`: Product type.
        - `coin`: Currency (valid when businessType is trans_from_exchange / trans_to_exchange).
        - `business_type`: Business type filter.
        - `only_funding`: Exclude non-financial businessType (yes/no).
        - `id_less_than`: Pagination, older data.
        - `start` / `end`: Time range (max 30 days).
        - `limit`: Page size, max 100, default 20.
        - `validate`: Whether to validate the response (default: True).

        > [Bitget API docs](https://www.bitget.com/api-doc/contract/account/Get-Account-Bill)
        """
        params = {'productType': product_type}
        if coin is not None:
            params['coin'] = coin
        if business_type is not None:
            params['businessType'] = business_type
        if only_funding is not None:
            params['onlyFunding'] = only_funding
        if id_less_than is not None:
            params['idLessThan'] = id_less_than
        if start is not None:
            params['startTime'] = ts.dump(start)
        if end is not None:
            params['endTime'] = ts.dump(end)
        if limit is not None:
            params['limit'] = str(limit)
        r = await self.authed_request('GET', '/api/v2/mix/account/bill', params=params)
        return self.output(r.text, validate_response, validate=validate)
