# Documentation

- **[Quickstart](quickstart.md)** — Install, credentials, first request
- **[Authentication](authentication.md)** — API keys and env vars
- **[API Overview](api-overview.md)** — Endpoints and modules
- **[Examples](examples.md)** — Portfolio, fills, tax, copy trading
- **[Design Philosophy](design-philosophy.md)** — Why we built it this way

## Quick start

```bash
pip install typed-bitget
export BITGET_ACCESS_KEY="..." BITGET_SECRET_KEY="..." BITGET_PASSPHRASE="..."
```

```python
from bitget import Bitget
async with Bitget.new() as client:
    assets = await client.spot.account.assets()
```

[Bitget API](https://www.bitget.com/api-doc/common/intro) · [Blog post](https://tribulnation.com/blog/clients)
