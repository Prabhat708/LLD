'''A food delivery application supports UPI, Credit Card, Cash and Wallet. Based on the user's selection, create the appropriate payment implementation.'''

from abc import ABC, abstractmethod

class PaymentOption(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(PaymentOption):
    def process_payment(self, amount):
        return f"Processing credit card payment of Rs.{amount}."

class UPI(PaymentOption):
    def process_payment(self, amount):
        return f"Processing UPI payment of Rs.{amount}."

class CashPayment(PaymentOption):
    def process_payment(self, amount):
        return f"Processing cash payment of Rs.{amount}."

class WalletPayment(PaymentOption):
    def process_payment(self, amount):
        return f"Processing wallet payment of Rs.{amount}."

class PaymentFactory:
    @staticmethod
    def payment_option(option):
        if option == "credit_card":
            return CreditCardPayment()
        elif option == "upi":
            return UPI()
        elif option == "cash":
            return CashPayment()
        elif option == "wallet":
            return WalletPayment()
        else:
            raise ValueError("Invalid payment option. Please choose 'credit_card', 'upi', 'cash', or 'wallet'.")

if __name__ == "__main__":
    option = input("Enter the payment option (credit_card, upi, cash, wallet): ").lower()
    amount = float(input("Enter the amount to be paid: "))
    try:
        payment_method = PaymentFactory.payment_option(option)
        print(payment_method.process_payment(amount))
    except ValueError as e:
        print("Payment method not available. Please choose a valid payment option.")

    