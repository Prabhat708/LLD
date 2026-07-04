from .PaymentStrategy import PaymentStrategy

class UpiPaymentStrategy(PaymentStrategy):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def pay(self, amount):
        print(f"Processing UPI payment of {amount} using UPI ID: {self.upi_id}")
