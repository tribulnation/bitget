from typing_extensions import TypeVar, Generic, Literal, TypeGuard
from dataclasses import dataclass, field
import json

from bitget.core import (
  HttpMixin, AuthHttpMixin, AuthHttpClient,
  ValidationMixin, validator, ApiError, TypedDict,
)

T = TypeVar('T')

BITGET_REST_URL = 'https://api.bitget.com'

class OkResponse(TypedDict, Generic[T]):
  code: Literal['00000']
  msg: Literal['success']
  requestTime: int
  data: T

class ErrResponse(TypedDict):
  code: str
  msg: str
  requestTime: int

Response = OkResponse[T] | ErrResponse

def is_ok(r: Response[T]) -> TypeGuard[OkResponse[T]]:
  return r['code'] == '00000' and r['msg'] == 'success'

def response_validator(type: type[T]) -> validator[Response[T]]:
  return validator(Response[type])

@dataclass
class BaseMixin(ValidationMixin):
  def output(self, data: str | bytes, validator: validator[Response[T]], validate: bool | None) -> T:
    obj = validator(data) if self.validate(validate) else json.loads(data)
    if not is_ok(obj):
      raise ApiError(obj)
    return obj['data']

@dataclass
class ApiMixin(BaseMixin, HttpMixin):
  base_url: str = field(kw_only=True, default=BITGET_REST_URL)

@dataclass
class ApiAuthMixin(BaseMixin, AuthHttpMixin):
  base_url: str = field(kw_only=True, default=BITGET_REST_URL)

  @classmethod
  def new(
    cls, access_key: str, secret_key: str, passphrase: str, *,
    base_url: str = BITGET_REST_URL, validate: bool = True,
  ):
    client = AuthHttpClient(access_key=access_key, secret_key=secret_key, passphrase=passphrase)
    return cls(base_url=base_url, auth_http=client, default_validate=validate)