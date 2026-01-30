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

### Spot Account

**Module**: `client.spot.account`

| Method | Description | Returns |
|--------|-------------|---------|
| `assets()` | Get spot account assets | `list[Asset]` |
| `deposit_records()` | Get deposit history | `DepositRecordsResponse` |
| `withdrawal_records()` | Get withdrawal history | `WithdrawalRecordsResponse` |

**Example:**

```python
# Get all spot assets
assets = await client.spot.account.assets()

# Get specific coin
usdt = await client.spot.account.assets(coin='USDT')

# Get only non-zero balances
held = await client.spot.account.assets(asset_type='hold_only')
```

### Spot Market

**Module**: `client.spot.market`

| Method | Description | Returns |
|--------|-------------|---------|
| `symbols()` | Get all trading pairs | `list[Symbol]` |

**Example:**

```python
# Get all symbols
symbols = await client.spot.market.symbols()

# Filter for BTC pairs
btc_pairs = [s for s in symbols if s['baseCoin'] == 'BTC']
```

### Spot Trade

**Module**: `client.spot.trade`

| Method | Description | Returns |
|--------|-------------|---------|
| `fills()` | Get trade fills | `FillsResponse` |

**Example:**

```python
from datetime import datetime, timedelta

end = datetime.now()
start = end - timedelta(days=7)

fills = await client.spot.trade.fills(
    symbol='BTCUSDT',
    start=start,
    end=end,
    limit=100
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
