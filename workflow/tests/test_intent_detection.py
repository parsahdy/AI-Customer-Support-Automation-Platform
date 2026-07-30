from workflow.intent_detector import detect_intent


message1 = "Where is my package."
print(f"Message 1 Intent: {detect_intent(message1)}")


message2 = "I want my money back."
print(f"Message 2 Intent: {detect_intent(message2)}")


message3 = "My account is locked."
print(f"Message 3 Intent: {detect_intent(message3)}")