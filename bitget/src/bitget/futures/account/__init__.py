from .account_list import AccountList
from .subaccount_assets import SubaccountAssets
from .single_account import SingleAccountEndpoint
from .bills import Bills

class Account(
  AccountList,
  SubaccountAssets,
  SingleAccountEndpoint,
  Bills
):
  ...