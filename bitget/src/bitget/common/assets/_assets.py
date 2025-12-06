from dataclasses import dataclass
from .assets_overview import AssetsOverview
from .bot_assets import BotAssets
from .funding_assets import FundingAssets

@dataclass
class Assets(
  AssetsOverview,
  BotAssets,
  FundingAssets
):
  ...