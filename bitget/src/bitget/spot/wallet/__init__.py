from .cancel_withdrawal import CancelWithdrawal
from .deposit_address import DepositAddress
from .deposit_records import DepositRecords
from .modify_deposit_account import ModifyDepositAccount
from .sub_transfer import SubTransfer
from .subaccount_deposit_address import SubaccountDepositAddress
from .transfer import Transfer
from .transfer_coin_info import TransferCoinInfo
from .withdrawal import Withdrawal
from .withdrawal_records import WithdrawalRecords

class Wallet(CancelWithdrawal, DepositAddress, DepositRecords, ModifyDepositAccount, SubTransfer, SubaccountDepositAddress, Transfer, TransferCoinInfo, Withdrawal, WithdrawalRecords):
  ...
