from .account_info import AccountInfo
from .assets import Assets
from .bills import Bills
from .deduct_info import DeductInfo
from .subaccount_assets import SubaccountAssets
from .transfer_records import TransferRecords

class Account(AccountInfo, Assets, Bills, DeductInfo, SubaccountAssets, TransferRecords):
  ...