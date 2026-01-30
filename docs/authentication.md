# Authentication

Set up your Bitget API credentials.

## Creating API Keys

1. Log into [Bitget](https://www.bitget.com) → Account → API Management → Create API
2. Set permissions (Read, Trade, Withdraw) and optionally IP whitelist
3. Save Access Key, Secret Key, and Passphrase (cannot be retrieved later)

## Providing Credentials

### Method 1: Environment Variables (Recommended)

```bash
export BITGET_ACCESS_KEY="bg_xxxxxxxxxxxxxx"
export BITGET_SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export BITGET_PASSPHRASE="your_passphrase"
```

```python
from bitget import Bitget
async with Bitget.new() as client:
    assets = await client.spot.account.assets()
```

### Method 2: .env File

Create `.env` (add to `.gitignore`), then:

```python
from dotenv import load_dotenv
load_dotenv()
from bitget import Bitget
async with Bitget.new() as client:
    assets = await client.spot.account.assets()
```

### Method 3: Explicit Parameters

```python
client = Bitget.new(
    access_key="...",
    secret_key="...",
    passphrase="..."
)
async with client:
    assets = await client.spot.account.assets()
```

## Testing Credentials

```python
async with Bitget.new() as client:
    await client.common.assets.overview()  # Raises AuthError if invalid
```

## Troubleshooting

- **KeyError: 'BITGET_ACCESS_KEY'** — Set env vars or pass credentials explicitly.
- **Invalid signature** — Check secret key; sync system time if needed.
- **IP not whitelisted** — Add your IP in Bitget API settings or disable restriction.

## Next Steps

- [Quickstart](quickstart.md) · [API Overview](api-overview.md) · [Examples](examples.md)
