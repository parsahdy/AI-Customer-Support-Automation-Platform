from workflow.decision_engine import decide_action


print(decide_action("returning_products", "high"))
print(decide_action("technical_support", "low"))
print(decide_action("order_tracking", "critical"))
print(decide_action("refund", "medium"))