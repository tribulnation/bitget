from bitget.core import AuthRouter
from .account import Account
from .public import Public
from .trade import Trade
from .wallet import Wallet

class Spot(AuthRouter):
  account: Account
  public: Public
  trade: Trade
  wallet: Wallet