from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict, Timestamp

class SubaccountAssetItem(TypedDict):
  coin: str
  available: Decimal
  limitAvailable: Decimal
  frozen: Decimal
  locked: Decimal
  uTime: Timestamp

class SubaccountAssetsItem(TypedDict):
  id: str | int  # API may return number
  userId: str
  assetsList: list[SubaccountAssetItem]

validate_response = validator(list[SubaccountAssetsItem])

@dataclass
class SubaccountAssets(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def subaccount_assets(self, *, id_less_than: str | None = None, limit: int | None = None, validate: bool | None = None) -> list[SubaccountAssetsItem]:
    params = {}
    if id_less_than is not None:
      params["idLessThan"] = id_less_than
    if limit is not None:
      params["limit"] = limit
    r = await self.authed_request("GET", "/api/v2/spot/account/subaccount-assets", params=params)
    return self.output(r.text, validate_response, validate=validate)
