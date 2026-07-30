from workflow.router import router


message1 = "I want my money back."
print(f"Message 1 workflow: {router(message1)}")


message2 = "Where is my order?."
print(f"Message 2 workflow: {router(message2)}")


message3 = "My application crashes."
print(f"Message 3 workflow: {router(message3)}")