from datetime import timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp

class MergeDepthData(TypedDict):
  asks: list[list[Decimal]]
  bids: list[list[Decimal]]
  precision: str
  scale: str
  isMaxPrecision: str
  ts: Timestamp

validate_response = validator(MergeDepthData)

@dataclass
class MergeDepth(Endpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def merge_depth(
    self,
    symbol: str,
    *,
    precision: str | None = None,
    limit: str | None = None,
    validate: bool | None = None
  ) -> MergeDepthData:
    """Get Merge Depth

    - `symbol`: Trading pair.
    - `precision`: scale0 / scale1 / scale2 / scale3. scale0 = no merge (default).
    - `limit`: 1 / 5 / 15 / 50 / max. Default 100.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Merge-Orderbook)
    """
    params: dict = {'symbol': symbol}
    if precision is not None:
      params['precision'] = precision
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v2/spot/market/merge-depth', params=params)
    return self.output(r.text, validate_response, validate=validate)
