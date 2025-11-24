import os
import asyncio
from dataclasses import dataclass
from .cross import Cross
from .isolated import Isolated

from bitget.core import BITGET_REST_URL, AuthHttpClient

@dataclass
class Margin:
  cross: Cross
  isolated: Isolated

  @classmethod
  def of(cls, auth_http: AuthHttpClient, *, base_url: str = BITGET_REST_URL, default_validate: bool = True):
    return cls(
      cross=Cross(auth_http=auth_http, base_url=base_url, default_validate=default_validate),
      isolated=Isolated(auth_http=auth_http, base_url=base_url, default_validate=default_validate),
    )

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
    return cls.of(auth_http=auth_http, base_url=base_url, default_validate=validate)
  
  async def __aenter__(self):
    await asyncio.gather(
      self.cross.__aenter__(),
      self.isolated.__aenter__(),
    )
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await asyncio.gather(
      self.cross.__aexit__(exc_type, exc_value, traceback),
      self.isolated.__aexit__(exc_type, exc_value, traceback),
    )