from .routes import INTENT_TO_WORKFLOW
from .intent_detector import detect_intent


def router(message: str) -> str:

    intent = detect_intent(message)

    workflow = INTENT_TO_WORKFLOW[intent]

    return workflow