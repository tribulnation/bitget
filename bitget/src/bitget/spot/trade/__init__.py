from .batch_cancel_orders import BatchCancelOrders
from .batch_cancel_replace_order import BatchCancelReplaceOrder
from .batch_place_orders import BatchPlaceOrders
from .cancel_order import CancelOrder
from .cancel_symbol_order import CancelSymbolOrder
from .fills import Fills
from .history_orders import HistoryOrders
from .order_info import OrderInfo
from .place_order import PlaceOrder
from .unfilled_orders import UnfilledOrders

class Trade(BatchCancelOrders, BatchCancelReplaceOrder, BatchPlaceOrders, CancelOrder, CancelSymbolOrder, Fills, HistoryOrders, OrderInfo, PlaceOrder, UnfilledOrders):
  ...