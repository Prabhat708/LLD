from .PaymentStrategy import PaymentStrategy

class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number, card_holder_name, expiry_date, cvv):
        self.card_number = card_number
        self.card_holder_name = card_holder_name
        self.expiry_date = expiry_date
        self.cvv = cvv

    def pay(self, amount):
        print(f"Processing credit card payment of {amount} using card number: {self.card_number}")