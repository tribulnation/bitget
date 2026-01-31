from .fills import Fills
from .order_detail import OrderDetailEndpoint
from .orders_pending import OrdersPending
from .orders_history import OrdersHistory
from .fill_history import FillHistory
from .place_order import PlaceOrder
from .cancel_order import CancelOrder

class Trade(Fills, OrderDetailEndpoint, OrdersPending, OrdersHistory, FillHistory, PlaceOrder, CancelOrder):
  ...

