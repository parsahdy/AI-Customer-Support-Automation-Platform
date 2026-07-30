"""
Mapping every Intent to it's workflow
"""


INTENT_TO_WORKFLOW = {
    "refund": "refund_workflow",
    "payment": "payment_workflow",
    "shipping": "shipping_workflow",
    "order_tracking": "tracking_workflow",
    "technical_support": "technical_workflow",
    "account": "account_workflow",
    "ordering": "ordering_workflow",
    "other": "human_review",
}