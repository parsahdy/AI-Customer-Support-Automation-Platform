from .intents import INTENT_KEYWORDS


def detect_intent(message: str) -> str:

    message = message.lower()

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message:
                return intent
