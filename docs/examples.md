# Examples

## Portfolio

```python
async with Bitget.new() as client:
    overview = await client.common.assets.overview()
    total = sum(a['usdtBalance'] for a in overview)
    print(f"Total: ${total:,.2f}")
```

## Positions & Fills

```python
# Futures positions
positions = await client.futures.position.all_positions(product_type='USDT-FUTURES')

# Recent spot fills
from datetime import datetime, timedelta
end, start = datetime.now(), datetime.now() - timedelta(days=7)
fills = await client.spot.trade.fills(start=start, end=end, limit=100)
```

## Tax Records

```python
start, end = datetime(2024, 1, 1), datetime(2024, 12, 31)
spot = await client.common.tax.spot_transaction_records(start=start, end=end)
futures = await client.common.tax.futures_transaction_records(start=start, end=end)
```

## Copy Trading

```python
spot_traders = await client.copy.spot.follower.my_traders()
futures_traders = await client.copy.futures.follower.my_traders()
```

## Pagination

```python
async for chunk in client.futures.trade.fills_paged(
    product_type='USDT-FUTURES', symbol='BTCUSDT'
):
    for fill in chunk:
        print(fill['price'], fill['baseVolume'])
```

## Error Handling

```python
from bitget.core import ApiError, ValidationError, NetworkError

try:
    assets = await client.spot.account.assets()
except ApiError as e:
    print(e)
except ValidationError:
    assets = await client.spot.account.assets(validate=False)
```

[API Overview](api-overview.md) · [Quickstart](quickstart.md)
