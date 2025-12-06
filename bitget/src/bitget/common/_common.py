from dataclasses import dataclass
from .assets import Assets
from .tax import Tax

@dataclass
class Common(Assets, Tax):
  ...