# Quickstart

## Installation

```bash
pip install typed-bitget
```

Requires Python 3.10+ and a [Bitget](https://www.bitget.com) account. Create an API key under Account → API Management and save Access Key, Secret Key, and Passphrase.

## Credentials

Set env vars (or use a `.env` file and `load_dotenv()`):

```bash
export BITGET_ACCESS_KEY="your_access_key"
export BITGET_SECRET_KEY="your_secret_key"
export BITGET_PASSPHRASE="your_passphrase"
```

## First Request

```python
import asyncio
from bitget import Bitget

async def main():
    async with Bitget.new() as client:
        assets = await client.spot.account.assets()
        for asset in assets:
            if asset['available'] > 0:
                print(f"{asset['coin']}: {asset['available']}")

asyncio.run(main())
```

## Client Structure

`client.spot`, `client.futures`, `client.margin`, `client.earn`, `client.copy`, `client.common` — each has sub-modules (e.g. `client.spot.account`, `client.spot.market`, `client.spot.trade`). Use `async with Bitget.new() as client:` for cleanup. Pass `access_key`, `secret_key`, `passphrase` to `Bitget.new()` if not using env vars. Use `validate=False` to skip response validation.

## Next Steps

[Authentication](authentication.md) · [API Overview](api-overview.md) · [Examples](examples.md)
