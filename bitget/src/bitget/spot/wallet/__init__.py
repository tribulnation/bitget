from .deposit_address import DepositAddress
from .deposit_records import DepositRecords
from .withdrawal_records import WithdrawalRecords

class Wallet(DepositAddress, DepositRecords, WithdrawalRecords):
  ...
