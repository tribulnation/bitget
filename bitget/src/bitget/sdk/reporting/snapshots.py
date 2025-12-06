from typing_extensions import NamedTuple, Sequence
from dataclasses import dataclass
from decimal import Decimal
from collections import Counter
from datetime import datetime
import asyncio

from trading_sdk.reporting import Snapshot, Snapshots as SnapshotsTDK

from bitget import Bitget
from bitget.sdk.core import SdkMixin

async def spot_balances(client: Bitget) -> Counter:
  balances = await client.spot.account.assets()
  return Counter({
    balance['coin']: balance['available'] + balance['frozen'] + balance['locked']
    for balance in balances
  })

async def futures_balances(client: Bitget) -> Counter:
  balances = Counter()
  for asset_type in ('USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES'):
    accounts = await client.futures.account.account_list(asset_type)
    for a in accounts:
      balances[a['marginCoin']] += Decimal(a['available']) # type: ignore

  for k, v in list(balances.items()):
    if v == 0:
      del balances[k]

  return balances

class Position(NamedTuple):
  size: Decimal
  entry: Decimal

async def futures_positions(client: Bitget) -> dict[str, Position]:
  positions: dict[str, Position] = {}
  for asset_type in ('USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES'):
    assets = await client.futures.position.all_positions(asset_type)
    for asset in assets:
      assert not asset['symbol'] in positions
      positions[asset['symbol']] = Position(
        size=asset['total'],
        entry=asset['openPriceAvg'],
      )
  
  return positions

async def earn_balances(client: Bitget) -> Counter:
  balances = await client.earn.account.assets()
  return Counter({
    balance['coin']: balance['amount']
    for balance in balances
  })

async def cross_margin_balances(client: Bitget) -> Counter:
  balances = await client.margin.cross.account_assets()
  return Counter({
    balance['coin']: balance['net']
    for balance in balances
  })

async def isolated_margin_balances(client: Bitget) -> Counter:
  balances = await client.margin.isolated.account_assets()
  return Counter({
    balance['coin']: balance['net']
    for balance in balances
  })

async def bot_balances(client: Bitget) -> Counter:
  balances = await client.common.bot_assets()
  return Counter({
    balance['coin']: balance['equity']
    for balance in balances
  })

async def funding_balances(client: Bitget) -> Counter:
  balances = await client.common.funding_assets()
  return Counter({
    balance['coin']: balance['available'] + balance['frozen']
    for balance in balances
  })

balance_functions = [
  spot_balances,
  futures_balances,
  earn_balances,
  cross_margin_balances,
  isolated_margin_balances,
  bot_balances,
  funding_balances,
]

async def all_balances(client: Bitget) -> Counter:
  balances = await asyncio.gather(*[fn(client) for fn in balance_functions])
  return sum(balances, start=Counter())

@dataclass
class Snapshots(SdkMixin, SnapshotsTDK):
  async def snapshots(self, assets: Sequence[str] = []) -> Sequence[Snapshot]:
    async with self.client:
      positions, balances = await asyncio.gather(
        futures_positions(self.client),
        all_balances(self.client),
      )
    
    time = datetime.now()
    return [
      Snapshot(asset=asset, time=time, qty=qty) # type: ignore
      for asset, qty in balances.items()
    ] + [
      Snapshot(asset=asset, time=time, qty=p.size, avg_price=p.entry)
      for asset, p in positions.items()
    ]
