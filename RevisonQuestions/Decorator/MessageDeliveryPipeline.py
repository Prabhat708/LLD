from abc import ABC, abstractmethod

class Message(ABC):

    @abstractmethod
    def sendMessage(self):
        pass  

class BasicMessage(Message):

    def __init__(self):
        self.attempts = 0

    def sendMessage(self):
        print("Sending message...")
        return True  # Simulating a successful message send

class MessageDecorator(Message):

    def __init__(self, message):
        self.message = message

class LoggingDecorator(MessageDecorator):

    def sendMessage(self):
        print("[LOG] Attempting to send message")
        return self.message.sendMessage()

class TimeStampDecorator(MessageDecorator):

    def sendMessage(self):
        from datetime import datetime
        print(f"[TIMESTAMP] {datetime.now()}")
        return self.message.sendMessage()

class PriorityDecorator(MessageDecorator):

    def sendMessage(self):
        print("[HIGH PRIORITY]")
        return self.message.sendMessage()
    
class RetryDecorator(MessageDecorator):

    def __init__(self, message, max_attempts=3):
        super().__init__(message)
        self.max_attempts = max_attempts

    def sendMessage(self):
        for attempt in range(1, self.max_attempts + 1):

            print(f"[RETRY] Attempt {attempt}")

            result = self.message.sendMessage()

            if result:
                return True

            if attempt < self.max_attempts:
                print("[RETRY] Retrying...")

        print("[RETRY] All attempts failed")
        return False

def main():
    message = BasicMessage()
    message = LoggingDecorator(message)
    message = TimeStampDecorator(message)
    message = PriorityDecorator(message)
    message = RetryDecorator(message, max_attempts=5)

    result = message.sendMessage()

    print("Final result:", "SUCCESS" if result else "FAILURE")


if __name__ == "__main__":
    main()

