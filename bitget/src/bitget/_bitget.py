import os
from dataclasses import dataclass
import asyncio

from bitget.core import BITGET_REST_URL, AuthHttpClient

from .common import Common
from .spot import Spot
from .futures import Futures
from .earn import Earn

@dataclass
class Bitget:
  common: Common
  spot: Spot
  futures: Futures
  earn: Earn

  @classmethod
  def new(
    cls, access_key: str | None = None, secret_key: str | None = None, passphrase: str | None = None, *,
    base_url: str = BITGET_REST_URL, validate: bool = True,
  ):
    if access_key is None:
      access_key = os.environ['BITGET_ACCESS_KEY']
    if secret_key is None:
      secret_key = os.environ['BITGET_SECRET_KEY']
    if passphrase is None:
      passphrase = os.environ['BITGET_PASSPHRASE']

    auth_http = AuthHttpClient(access_key=access_key, secret_key=secret_key, passphrase=passphrase)
    return cls(
      common=Common(auth_http=auth_http, base_url=base_url, default_validate=validate),
      spot=Spot(auth_http=auth_http, base_url=base_url, default_validate=validate),
      futures=Futures(auth_http=auth_http, base_url=base_url, default_validate=validate),
      earn=Earn(auth_http=auth_http, base_url=base_url, default_validate=validate),
    )
  
  async def __aenter__(self):
    await asyncio.gather(
      self.common.__aenter__(),
      self.spot.__aenter__(),
      self.futures.__aenter__(),
      self.earn.__aenter__(),
    )
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await asyncio.gather(
      self.common.__aexit__(exc_type, exc_value, traceback),
      self.spot.__aexit__(exc_type, exc_value, traceback),
      self.futures.__aexit__(exc_type, exc_value, traceback),
      self.earn.__aexit__(exc_type, exc_value, traceback),
    )