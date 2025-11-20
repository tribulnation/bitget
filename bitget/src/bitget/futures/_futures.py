from dataclasses import dataclass
from .account import Account
from .position import Position

@dataclass
class Futures(Account, Position):
  ...