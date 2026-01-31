from datetime import timedelta
from dataclasses import dataclass

from bitget.core import Endpoint, rate_limit, validator, TypedDict, Timestamp

class ServerTimeData(TypedDict):
  serverTime: Timestamp

validate_response = validator(ServerTimeData)

@dataclass
class ServerTime(Endpoint):
  @rate_limit(timedelta(seconds=1/20))
  async def server_time(self, *, validate: bool | None = None) -> ServerTimeData:
    """Get Server Time

    Getting server time, Unix millisecond timestamp.

    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [Bitget API docs](https://www.bitget.com/api-doc/spot/public/Get-Server-Time)
    """
    r = await self.request('GET', '/api/v2/public/time')
    return self.output(r.text, validate_response, validate=validate)
