# Design Philosophy

Typed Bitget follows four principles from [this blog post](https://tribulnation.com/blog/clients) on building better API clients.

## 1. Inputs shouldn't require custom imports

Use string literals, not enums. Your IDE autocompletes from `Literal` types:

```python
positions = await client.futures.position.all_positions(product_type='USDT-FUTURES')
```

## 2. Annotate types precisely

`TypedDict` with `Decimal` for prices, `datetime` for timestamps, `Literal` for enums. IDE and type checkers know exactly what you get.

## 3. Avoid unnecessary complication

Sensible defaults: `Bitget.new()` uses env vars and `https://api.bitget.com`. Override only when needed (`base_url=`, `validate=False`).

## 4. Provide extra behavior optionally

Validation is on by default; use `validate=False` to skip. Pagination helpers exist (`fills_paged`) but simple `fills()` is there too. No forced retries or caching.

---

**Details matter. Developer experience matters.** Read the full post: [tribulnation.com/blog/clients](https://tribulnation.com/blog/clients)

[API Overview](api-overview.md) · [Examples](examples.md)
