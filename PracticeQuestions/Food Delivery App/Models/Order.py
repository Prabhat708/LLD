from abc import ABC, abstractmethod


class Order(ABC):
    next_order_id = 0

    def __init__(self):
        self.user = None
        self.restaurant = None
        self.items = []
        self.payment_strategy = None
        self.total = 0.0
        self.scheduled = ""

        Order.next_order_id += 1
        self.order_id = Order.next_order_id

    def __del__(self):
        self.payment_strategy = None

    def process_payment(self):
        if self.payment_strategy:
            self.payment_strategy.pay(self.total)
            return True
        else:
            print("Please choose a payment mode first")
            return False

    @abstractmethod
    def get_type(self):
        pass

    # Getters and Setters
    def get_order_id(self):
        return self.order_id

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def set_restaurant(self, restaurant):
        self.restaurant = restaurant

    def get_restaurant(self):
        return self.restaurant

    def set_items(self, items):
        self.items = items
        self.total = 0

        for item in self.items:
            self.total += item.get_price()

    def get_items(self):
        return self.items

    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def set_scheduled(self, scheduled):
        self.scheduled = scheduled

    def get_scheduled(self):
        return self.scheduled

    def get_total(self):
        return self.total

    def set_total(self, total):
        self.total = total