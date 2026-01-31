from .candles import Candles
from .history_candles import HistoryCandles
from .market_trades import MarketTrades
from .merge_depth import MergeDepth
from .orderbook import Orderbook
from .recent_trades import RecentTrades
from .tickers import Tickers
from .vip_fee_rate import VipFeeRate

class Market(Candles, HistoryCandles, MarketTrades, MergeDepth, Orderbook, RecentTrades, Tickers, VipFeeRate):
  ...
