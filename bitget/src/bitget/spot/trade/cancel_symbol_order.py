from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class CancelSymbolOrderData(TypedDict):
  symbol: str

validate_response = validator(CancelSymbolOrderData)

@dataclass
class CancelSymbolOrder(AuthEndpoint):
  @rate_limit(timedelta(seconds=1/5))
  async def cancel_symbol_order(
    self,
    symbol: str,
    *,
    validate: bool | None = None
  ) -> CancelSymbolOrderData:
    """Cancel all orders for a symbol.

    - `symbol`: Trading pair, e.g. USDCUSDT.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/trade/Cancel-Symbol-Orders)
    """
    r = await self.authed_request('POST', '/api/v2/spot/trade/cancel-symbol-order', json={'symbol': symbol})
    return self.output(r.text, validate_response, validate=validate)
