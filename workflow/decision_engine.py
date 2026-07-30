from .decision_rules import DECISION_RULES


def decide_action(intent: str, priority: str) -> dict:

    rule = DECISION_RULES.get(intent, DECISION_RULES.get("other"))

    if priority.lower() in ("high", "critical"):
        action = rule.get("high_priority", rule.get("default"))
    else:
        action = rule.get("normal", rule.get("default"))

    return {
        "workflow": rule["workflow"],
        "action": action,
    }