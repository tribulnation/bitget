from dataclasses import dataclass
from .account_list import AccountList
from .subaccount_assets import SubaccountAssets

@dataclass
class Account(
  AccountList,
  SubaccountAssets
):
  ...