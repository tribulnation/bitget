from .symbols import Symbols
from .ticker import Ticker
from .tickers import Tickers
from .merge_depth import MergeDepth

class Market(Symbols, Ticker, Tickers, MergeDepth):
  ...