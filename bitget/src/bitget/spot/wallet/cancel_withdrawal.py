from dataclasses import dataclass
from datetime import timedelta

from bitget.core import AuthEndpoint, rate_limit, validator, TypedDict

class CancelWithdrawalData(TypedDict):
  data: str  # success / fail

validate_response = validator(CancelWithdrawalData)

@dataclass
class CancelWithdrawal(AuthEndpoint):
  @rate_limit(timedelta(seconds=0.1))
  async def cancel_withdrawal(
    self,
    order_id: str,
    *,
    validate: bool | None = None
  ) -> CancelWithdrawalData:
    """Cancel Withdrawal

    Subject to review status and user settings; small auto withdrawals cannot be revoked.

    - `order_id`: Withdraw orderId.
    - `validate`: Whether to validate the response (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/account/Cancel-Withdrawal)
    """
    json_body: dict = {'orderId': order_id}
    r = await self.authed_request('POST', '/api/v2/spot/wallet/cancel-withdrawal', json=json_body)
    return self.output(r.text, validate_response, validate=validate)
