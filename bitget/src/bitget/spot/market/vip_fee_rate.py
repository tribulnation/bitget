from datetime import timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict

class VipFeeRateItem(TypedDict):
  level: str
  dealAmount: Decimal
  assetAmount: Decimal
  takerFeeRate: Decimal
  makerFeeRate: Decimal
  btcWithdrawAmount: Decimal
  usdtWithdrawAmount: Decimal

validate_response = validator(list[VipFeeRateItem])

@dataclass
class VipFeeRate(Endpoint):
  @rate_limit(timedelta(seconds=1/10))
  async def vip_fee_rate(self, *, validate: bool | None = None) -> list[VipFeeRateItem]:
    """Get VIP Fee Rate

    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-VIP-Fee-Rate)
    """
    r = await self.request('GET', '/api/v2/spot/market/vip-fee-rate')
    return self.output(r.text, validate_response, validate=validate)
