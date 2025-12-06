from bitget.core import AuthRouter
from .common import Common
from .spot import Spot
from .futures import Futures
from .earn import Earn
from .margin import Margin

class Bitget(AuthRouter):
  common: Common
  spot: Spot
  futures: Futures
  earn: Earn
  margin: Margin