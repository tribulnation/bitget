from .batch_cancel_plan_order import BatchCancelPlanOrder
from .current_plan_orders import CurrentPlanOrders
from .history_plan_orders import HistoryPlanOrders
from .modify_plan_order import ModifyPlanOrder
from .place_plan_order import PlacePlanOrder

class Trigger(BatchCancelPlanOrder, CurrentPlanOrders, HistoryPlanOrders, ModifyPlanOrder, PlacePlanOrder):
  ...
