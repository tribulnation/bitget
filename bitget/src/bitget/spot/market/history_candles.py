from datetime import datetime, timedelta
from dataclasses import dataclass
from decimal import Decimal

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp, timestamp as ts

class CandleItem(TypedDict):
  ts: Timestamp
  open: Decimal
  high: Decimal
  low: Decimal
  close: Decimal
  baseVolume: Decimal
  usdtVolume: Decimal
  quoteVolume: Decimal

def _candle_row(v: list) -> CandleItem:
  return {
    'ts': ts.parse(v[0]),
    'open': Decimal(v[1]),
    'high': Decimal(v[2]),
    'low': Decimal(v[3]),
    'close': Decimal(v[4]),
    'baseVolume': Decimal(v[5]),
    'usdtVolume': Decimal(v[6]),
    'quoteVolume': Decimal(v[7]),
  }

@dataclass
class HistoryCandles(Endpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def history_candles(
    self,
    symbol: str,
    granularity: str,
    end: datetime,
    *,
    limit: int | None = None,
    validate: bool | None = None
  ) -> list[CandleItem]:
    """Get History Candlestick Data

    - `symbol`: Trading pair.
    - `granularity`: 1min, 3min, 5min, 15min, 30min, 1h, 4h, 6h, 12h, 1day, 3day, 1week, 1M, etc.
    - `end`: End time (get data before this timestamp).
    - `limit`: Default 100, max 200.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/market/Get-History-Candle-Data)
    """
    params: dict = {'symbol': symbol, 'granularity': granularity, 'endTime': ts.dump(end)}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v2/spot/market/history-candles', params=params)
    raw = self.output(r.text, validator(list), validate=False)
    return [_candle_row(row) for row in raw]
