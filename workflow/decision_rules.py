DECISION_RULES = {
    
    "refund": {
        "workflow": "refund_workflow",
        "high_priority": "human",
        "normal": "rag",
    },

    "technical_support": {
        "workflow": "technical_workflow",
        "high_priority": "human",
        "normal": "rag",
    },

    "order_tracking": {
        "workflow": "tracking_workflow",
        "default": "tracking_api",
    },

    "payment": {
        "workflow": "payment_workflow",
        "default": "rag",
    },

    "ordering": {
        "workflow": "ordering_workflow",
        "default": "rag",
    },

    "shipping": {
        "workflow": "shipping_workflow",
        "default": "rag",
    },

    "other": {
        "workflow": "human_review",
        "default": "human",
    },
}
