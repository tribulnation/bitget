# API Overview

Guide to available endpoints in Typed Bitget. Not all [Bitget API](https://www.bitget.com/api-doc/common/intro) endpoints are implemented yet.

## Module Structure

The client is organized hierarchically, mirroring Bitget's API structure:

```python
from bitget import Bitget

async with Bitget.new() as client:
    client.spot          # Spot trading
    client.futures       # Futures trading
    client.margin        # Margin trading
    client.earn          # Earn (savings/staking)
    client.copy          # Copy trading
    client.common        # Common endpoints (cross-product)
```

## Spot Trading

### Spot Public

**Module**: `client.spot.public`

| Method | Description | Returns |
|--------|-------------|---------|
| `server_time()` | Get server time | `datetime` |
| `coins()` | Get coin list | `list` |
| `symbols()` | Get trading pairs | `list[Symbol]` |

### Spot Market

**Module**: `client.spot.market`

| Method | Description | Returns |
|--------|-------------|---------|
| `vip_fee_rate()` | Get VIP fee rate | — |
| `tickers()` | Get ticker info | `list[TickerItem]` |
| `orderbook()` | Get order book depth | `OrderbookData` |
| `merge_depth()` | Get merged order book depth | `MergeDepthData` |
| `candles()` | Get candlestick data | `list` |
| `history_candles()` | Get historical candles | `list` |
| `recent_trades()` | Get recent trades | `list[RecentTradeItem]` |
| `market_trades()` | Get market trades history | `list[MarketTradeItem]` |

### Spot Account

**Module**: `client.spot.account`

| Method | Description | Returns |
|--------|-------------|---------|
| `account_info()` | Get account information | — |
| `assets()` | Get spot account assets | `list[Asset]` |
| `bills()` | Get account bills | `list` |
| `subaccount_assets()` | Get sub-accounts assets (assets > 0) | `list[SubaccountAssetsItem]` |
| `transfer_records()` | Get transfer record | `list[TransferRecordItem]` |
| `deduct_info()` | Get BGB deduct info | `DeductInfoData` |

**Example:**

```python
# Get all spot assets
assets = await client.spot.account.assets()

# Get specific coin
usdt = await client.spot.account.assets(coin='USDT')

# Get only non-zero balances
held = await client.spot.account.assets(asset_type='hold_only')

# Sub-accounts with balance
subs = await client.spot.account.subaccount_assets()
```

### Spot Trade

**Module**: `client.spot.trade`

| Method | Description | Returns |
|--------|-------------|---------|
| `place_order()` | Place order | `PlaceOrderData` |
| `cancel_order()` | Cancel order | `CancelOrderData` |
| `batch_place_orders()` | Batch place orders | `BatchPlaceOrderData` |
| `batch_cancel_orders()` | Batch cancel orders | `BatchCancelOrdersData` |
| `batch_cancel_replace_order()` | Cancel and replace (batch) | `list[BatchCancelReplaceItemResult]` |
| `cancel_symbol_order()` | Cancel all orders for symbol | — |
| `order_info()` | Get order info | `list[OrderInfoItem]` |
| `unfilled_orders()` | Get current (unfilled) orders | `list[UnfilledOrderItem]` |
| `history_orders()` | Get history orders | `list[HistoryOrderItem]` |
| `fills()` | Get fills | `list[Fill]` |
| `fills_paged()` | Get fills (paginated) | `AsyncGenerator` |

**Example:**

```python
from datetime import datetime, timedelta

# Place limit order (use symbol price precision)
symbols = await client.spot.public.symbols(symbol='USDCUSDT')
prec = int(symbols[0]['pricePrecision'])
place = await client.spot.trade.place_order(
    'USDCUSDT', 'buy', 'limit', '5',
    price=str(round(1.0 - 0.01, prec))
)
oid = place['orderId']
await client.spot.trade.cancel_order('USDCUSDT', order_id=oid)

# Fills
fills = await client.spot.trade.fills(symbol='USDCUSDT', limit=100)
async for chunk in client.spot.trade.fills_paged(symbol='USDCUSDT', limit=20):
    ...
```

### Spot Trigger (Plan Orders)

**Module**: `client.spot.trigger`

| Method | Description | Returns |
|--------|-------------|---------|
| `place_plan_order()` | Place plan order | `PlacePlanOrderData` |
| `modify_plan_order()` | Modify plan order | `ModifyPlanOrderData` |
| `current_plan_orders()` | Get current plan orders | `CurrentPlanOrdersData` |
| `history_plan_orders()` | Get history plan orders | `HistoryPlanOrdersData` |
| `batch_cancel_plan_order()` | Batch cancel plan orders | `BatchCancelPlanOrderData` |

### Spot Wallet

**Module**: `client.spot.wallet`

| Method | Description | Returns |
|--------|-------------|---------|
| `modify_deposit_account()` | Modify deposit account (auto-transfer) | — |
| `sub_transfer()` | Sub-account transfer | `SubTransferData` |
| `subaccount_deposit_address()` | Get sub-account deposit address | — |
| `deposit_address()` | Get deposit address | — |
| `deposit_records()` | Get deposit history | — |
| `withdrawal_records()` | Get withdrawal history | — |
| `transfer()` | Transfer between product types | `TransferData` |
| `transfer_coin_info()` | Get transferable coin list | `list[str]` |
| `withdrawal()` | Withdraw (on-chain or internal) | `WithdrawalData` |
| `cancel_withdrawal()` | Cancel withdrawal | `CancelWithdrawalData` |

**Example:**

```python
# Transfer spot -> isolated margin (symbol required for margin)
await client.spot.wallet.transfer(
    'spot', 'isolated_margin', '100', 'USDT',
    symbol='BTCUSDT'
)

# Transferable coins between two account types
coins = await client.spot.wallet.transfer_coin_info(
    'spot', 'isolated_margin'
)
```

## Futures Trading

### Futures Account

**Module**: `client.futures.account`

| Method | Description | Returns |
|--------|-------------|---------|
| `account_list()` | List futures accounts | `list[Account]` |
| `subaccount_assets()` | Get subaccount assets | `list[SubaccountAsset]` |

**Example:**

```python
# Get all futures accounts
accounts = await client.futures.account.account_list(
    product_type='USDT-FUTURES'
)

# Check margin tier
for account in accounts:
    print(f"{account['marginCoin']}: {account['crossMaxAvailable']}")
```

### Futures Market

**Module**: `client.futures.market`

| Method | Description | Returns |
|--------|-------------|---------|
| `symbols()` | Get futures symbols | `list[Symbol]` |

**Example:**

```python
# Get all USDT futures
symbols = await client.futures.market.symbols(
    product_type='USDT-FUTURES'
)
```

### Futures Positions

**Module**: `client.futures.position`

| Method | Description | Returns |
|--------|-------------|---------|
| `all_positions()` | Get all positions | `list[Position]` |

**Example:**

```python
# Get all USDT futures positions
positions = await client.futures.position.all_positions(
    product_type='USDT-FUTURES'
)

# Get specific symbol
btc_position = await client.futures.position.all_positions(
    product_type='USDT-FUTURES',
    symbol='BTCUSDT'
)
```

### Futures Trade

**Module**: `client.futures.trade`

| Method | Description | Returns |
|--------|-------------|---------|
| `fills()` | Get trade fills | `FillsResponse` |
| `fills_paged()` | Auto-paginated fills | `AsyncGenerator` |
| `all_fills_paged()` | Fills across all product types | `AsyncGenerator` |

**Example:**

```python
# Simple query
fills = await client.futures.trade.fills(
    product_type='USDT-FUTURES',
    symbol='BTCUSDT'
)

# Auto-paginated (yields chunks)
async for chunk in client.futures.trade.fills_paged(
    product_type='USDT-FUTURES',
    symbol='BTCUSDT',
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31)
):
    for fill in chunk:
        print(f"Price: {fill['price']}, Volume: {fill['baseVolume']}")

# All product types
async for chunk in client.futures.trade.all_fills_paged():
    process_fills(chunk)
```

## Margin Trading

### Cross Margin

**Module**: `client.margin.cross.account`

| Method | Description | Returns |
|--------|-------------|---------|
| `assets()` | Get cross margin assets | `list[Asset]` |

**Module**: `client.margin.cross.trade`

| Method | Description | Returns |
|--------|-------------|---------|
| `fills()` | Get cross margin fills | `FillsResponse` |

### Isolated Margin

**Module**: `client.margin.isolated.account`

| Method | Description | Returns |
|--------|-------------|---------|
| `assets()` | Get isolated margin assets | `list[Asset]` |

**Module**: `client.margin.isolated.trade`

| Method | Description | Returns |
|--------|-------------|---------|
| `fills()` | Get isolated margin fills | `FillsResponse` |

**Example:**

```python
# Cross margin assets
cross_assets = await client.margin.cross.account.assets()

# Isolated margin for specific pair
isolated_assets = await client.margin.isolated.account.assets(
    symbol='BTCUSDT'
)
```

## Earn

### Earn Account

**Module**: `client.earn.account`

| Method | Description | Returns |
|--------|-------------|---------|
| `assets()` | Get earn account assets | `list[Asset]` |

### Savings Products

**Module**: `client.earn.savings`

| Method | Description | Returns |
|--------|-------------|---------|
| `products()` | Get available savings products | `list[Product]` |

**Example:**

```python
# Get earn balance
earn_assets = await client.earn.account.assets()

# Browse savings products
products = await client.earn.savings.products()

for product in products:
    print(f"{product['coin']}: {product['rate']}% APY")
```

## Copy Trading

### Spot Copy Trading

**Module**: `client.copy.spot.follower`

| Method | Description | Returns |
|--------|-------------|---------|
| `my_traders()` | Get traders you're following | `MyTradersResponse` |

### Futures Copy Trading

**Module**: `client.copy.futures.follower`

| Method | Description | Returns |
|--------|-------------|---------|
| `my_traders()` | Get traders you're following | `MyTradersResponse` |

**Example:**

```python
# Get spot copy traders
spot_traders = await client.copy.spot.follower.my_traders()

# Get futures copy traders
futures_traders = await client.copy.futures.follower.my_traders(
    page_size=20,
    page_no=1
)
```

## Common Endpoints

### Assets

**Module**: `client.common.assets`

| Method | Description | Returns |
|--------|-------------|---------|
| `overview()` | Get all account balances | `list[AssetOverview]` |
| `bot()` | Get bot account info | `BotAssets` |
| `funding()` | Get funding account | `FundingAssets` |

**Example:**

```python
# Portfolio overview (all accounts)
overview = await client.common.assets.overview()

total = sum(account['usdtBalance'] for account in overview)
print(f"Total Balance: ${total:,.2f}")

# By account type
for account in overview:
    print(f"{account['accountType']}: ${account['usdtBalance']}")
```

### Tax Records

**Module**: `client.common.tax`

| Method | Description | Returns |
|--------|-------------|---------|
| `spot_transaction_records()` | Get spot transaction records | `Records` |
| `futures_transaction_records()` | Get futures records | `Records` |
| `margin_transaction_records()` | Get margin records | `Records` |
| `p2p_transaction_records()` | Get P2P records | `Records` |

**Example:**

```python
from datetime import datetime

# Tax year 2024
start = datetime(2024, 1, 1)
end = datetime(2024, 12, 31)

# Get all transaction types
spot = await client.common.tax.spot_transaction_records(
    start=start, end=end
)
futures = await client.common.tax.futures_transaction_records(
    start=start, end=end
)
margin = await client.common.tax.margin_transaction_records(
    start=start, end=end
)
```

## Common Parameters

- **product_type**: `'USDT-FUTURES'`, `'COIN-FUTURES'`, `'USDC-FUTURES'`, `'SPOT'`
- **Time**: Pass `datetime` or ms; e.g. `start=datetime(2024,1,1)`, `end=datetime.now()`
- **validate**: Default `True`; use `validate=False` per call or `Bitget.new(validate=False)` to skip Pydantic validation

## Response Types

Responses are `TypedDict` (e.g. `Decimal` for amounts, `datetime` for timestamps). Use IDE autocomplete.

## Pagination

Manual: use `id_less_than=resp['endId']` for next page. Auto: `async for chunk in client.futures.trade.fills_paged(...):`

## Errors

`bitget.core`: `Error`, `NetworkError`, `ValidationError`, `UserError`, `AuthError`, `ApiError`. Catch as needed.

## Advanced

Custom base URL: `Bitget.new(..., base_url='https://testnet-api.bitget.com')`. Manual HTTP: pass `http=AuthHttpClient(...)`.

## Next Steps

[Examples](examples.md) · [Design Philosophy](design-philosophy.md) · [Quickstart](quickstart.md)

For parameter details, use `help(client.spot.account.assets)` or your IDE docstrings.
