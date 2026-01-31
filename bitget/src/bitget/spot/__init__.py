from bitget.core import AuthRouter
from .account import Account
from .market import Market
from .public import Public
from .trade import Trade
from .trigger import Trigger
from .wallet import Wallet

class Spot(AuthRouter):
  account: Account
  market: Market
  public: Public
  trade: Trade
  trigger: Trigger
  wallet: Wallet