from abc import ABC, abstractmethod

# ============================
#       Notification & Decorators
# ============================

class INotification(ABC):
    @abstractmethod
    def get_content(self):
        pass


# Concrete Notification: simple text notification.
class SimpleNotification(INotification):
    def __init__(self, msg):
        self.text = msg

    def get_content(self):
        return self.text


# Abstract Decorator: wraps a Notification object.
class INotificationDecorator(INotification):
    def __init__(self, notification):
        self.notification = notification

    def __del__(self):
        # Python's garbage collector handles cleanup automatically.
        self.notification = None


# Decorator to add a timestamp to the content.
class TimestampDecorator(INotificationDecorator):
    def get_content(self):
        return (
            "[2025-04-13 14:22:00] "
            + self.notification.get_content()
        )


# Decorator to append a signature to the content.
class SignatureDecorator(INotificationDecorator):
    def __init__(self, notification, signature):
        super().__init__(notification)
        self.signature = signature

    def get_content(self):
        return (
            self.notification.get_content()
            + f"\n-- {self.signature}\n\n"
        )

# ============================
#      Observer Pattern Components
# ============================

# Observer interface: each observer gets an update with a Notification.
class IObserver(ABC):
    @abstractmethod
    def update(self):
        pass


# Observable interface
class IObservable(ABC):
    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


# Concrete Observable
class NotificationObservable(IObservable):
    def __init__(self):
        self.observers = []
        self.current_notification = None

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

    def set_notification(self, notification):
        self.current_notification = notification
        self.notify_observers()

    def get_notification(self):
        return self.current_notification

    def get_notification_content(self):
        if self.current_notification is None:
            return ""
        return self.current_notification.get_content()

# ============================
#       NotificationService
# ============================

# The NotificationService manages notifications. It keeps track of notifications.
# Any client code will interact with this service.


# Singleton class
class NotificationService:
    _instance = None

    def __init__(self):
        # Private constructor
        self.observable = NotificationObservable()
        self.notifications = []

    @staticmethod
    def get_instance():
        if NotificationService._instance is None:
            NotificationService._instance = NotificationService()
        return NotificationService._instance

    # Expose the observable so observers can attach.
    def get_observable(self):
        return self.observable

    # Creates a new Notification and notifies observers.
    def send_notification(self, notification):
        self.notifications.append(notification)
        self.observable.set_notification(notification)

    def __del__(self):
        self.observable = None


# ============================
#       Concrete Observers
# ============================

class Logger(IObserver):
    def __init__(self, observable=None):
        if observable is None:
            self.notification_observable = (
                NotificationService.get_instance().get_observable()
            )
        else:
            self.notification_observable = observable

        self.notification_observable.add_observer(self)

    def update(self):
        print(
            "Logging New Notification :\n"
            + self.notification_observable.get_notification_content()
        )


# ============================
#   Strategy Pattern Components
# ============================

# Abstract class for different Notification Strategies.
class INotificationStrategy(ABC):
    @abstractmethod
    def send_notification(self, content):
        pass


class EmailStrategy(INotificationStrategy):
    def __init__(self, email_id):
        self.email_id = email_id

    def send_notification(self, content):
        # Simulate the process of sending an email notification,
        # representing the dispatch of messages to users via email.
        print(
            f"Sending Email Notification to: {self.email_id}\n"
            f"{content}"
        )


class SMSStrategy(INotificationStrategy):
    def __init__(self, mobile_number):
        self.mobile_number = mobile_number

    def send_notification(self, content):
        # Simulate the process of sending an SMS notification,
        # representing the dispatch of messages to users via SMS.
        print(
            f"Sending SMS Notification to: {self.mobile_number}\n"
            f"{content}"
        )


class PopUpStrategy(INotificationStrategy):
    def send_notification(self, content):
        # Simulate the process of sending popup notification.
        print(f"Sending Popup Notification:\n{content}")


# Concrete Observer
class NotificationEngine(IObserver):
    def __init__(self, observable=None):
        if observable is None:
            self.notification_observable = (
                NotificationService.get_instance().get_observable()
            )
        else:
            self.notification_observable = observable

        self.notification_observable.add_observer(self)

        self.notification_strategies = []

    def add_notification_strategy(self, strategy):
        self.notification_strategies.append(strategy)

    # Can have remove_notification_strategy() as well.

    def update(self):
        notification_content = (
            self.notification_observable.get_notification_content()
        )

        for strategy in self.notification_strategies:
            strategy.send_notification(notification_content)


def main():
    # Create NotificationService.
    notification_service = NotificationService.get_instance()

    # Create Logger Observer.
    logger = Logger()

    # Create NotificationEngine Observer.
    notification_engine = NotificationEngine()

    notification_engine.add_notification_strategy(
        EmailStrategy("random.person@gmail.com")
    )

    notification_engine.add_notification_strategy(
        SMSStrategy("+91 9876543210")
    )

    notification_engine.add_notification_strategy(
        PopUpStrategy()
    )

    # Create a notification with decorators.
    notification = SimpleNotification("Your order has been shipped!")
    notification = TimestampDecorator(notification)
    notification = SignatureDecorator(notification, "Customer Care")

    notification_service.send_notification(notification)


if __name__ == "__main__":
    main()



"""
==========================================================
              Notification System Architecture
==========================================================

                    NotificationService (Singleton)
                               │
                               ▼
                  NotificationObservable (Subject)
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
          Logger (Observer)        NotificationEngine (Observer)
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                       EmailStrategy   SMSStrategy   PopUpStrategy
                                              ▲
                                              │
                                   Decorated Notification
                                              ▲
                                  SignatureDecorator
                                              ▲
                                  TimestampDecorator
                                              ▲
                                  SimpleNotification

==========================================================
Execution Flow
==========================================================

1. Client creates a notification.

    notification = SimpleNotification(...)
    notification = TimestampDecorator(notification)
    notification = SignatureDecorator(notification, "Customer Care")

Decorator Chain:

    SignatureDecorator
            │
            ▼
    TimestampDecorator
            │
            ▼
    SimpleNotification


2. Client sends notification.

    NotificationService.send_notification(notification)


3. NotificationService stores the notification and forwards it
   to NotificationObservable.

    NotificationService
            │
            ▼
    NotificationObservable


4. Observable notifies every registered observer.

    notify_observers()
            │
            ├────────► Logger.update()
            │
            └────────► NotificationEngine.update()


5. Logger simply logs the notification.

    Logging New Notification...


6. NotificationEngine delegates notification delivery
   to all configured strategies.

    NotificationEngine
            │
            ├────────► EmailStrategy
            ├────────► SMSStrategy
            └────────► PopUpStrategy


==========================================================
Design Patterns Used
==========================================================

1. Singleton
   - NotificationService
   - Only one notification service exists.

2. Observer
   - Subject:
       NotificationObservable

   - Observers:
       Logger
       NotificationEngine

   - Whenever a new notification arrives,
     all observers are notified automatically.

3. Strategy
   - NotificationEngine delegates the delivery
     to different strategies.

   Strategies:
       • EmailStrategy
       • SMSStrategy
       • PopUpStrategy

   New strategies (WhatsApp, Slack, Push, etc.)
   can be added without modifying NotificationEngine.

4. Decorator
   - SimpleNotification is the base object.
   - TimestampDecorator adds timestamp.
   - SignatureDecorator adds signature.

   Features are added dynamically without modifying
   the original Notification class.

==========================================================
Pattern Responsibilities
==========================================================

Singleton  -> One NotificationService instance.

Observer   -> Decides WHO receives the notification.

Strategy   -> Decides HOW the notification is delivered.

Decorator  -> Decides WHAT extra information is added
              to the notification.
==========================================================
"""