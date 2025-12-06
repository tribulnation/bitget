from bitget.core import AuthRouter
from .account import Account
from .position import Position

class Futures(AuthRouter):
  account: Account
  position: Position