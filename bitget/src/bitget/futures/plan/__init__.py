from .orders_plan_pending import OrdersPlanPending
from .orders_plan_history import OrdersPlanHistory
from .plan_sub_orders import PlanSubOrders

class Plan(OrdersPlanPending, OrdersPlanHistory, PlanSubOrders):
    ...
