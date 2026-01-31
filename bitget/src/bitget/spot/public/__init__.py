from .symbols import Symbols
from .coins import Coins
from .server_time import ServerTime

class Public(Symbols, Coins, ServerTime):
  ...