from abc import ABC, abstractmethod

class ProcessPayment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class OwnPaymentGateway(ProcessPayment):
    def pay(self, amount):
        print(f"Processing payment of Rs. {amount} through OwnPaymentGateway.")

class ThirdPartyPaymentGateway:
    def make_payment(self, amount):
        print(f"Processing payment of Rs. {amount} through ThirdPartyPaymentGateway.")

class ThirdPartyPaymentAdapter(ProcessPayment):
    def __init__(self, third_party_gateway):
        self.third_party_gateway = third_party_gateway

    def pay(self, amount):
        self.third_party_gateway.make_payment(amount)

def main():
    own_gateway = OwnPaymentGateway()
    own_gateway.pay(100)

    third_party_gateway = ThirdPartyPaymentGateway()
    adapter = ThirdPartyPaymentAdapter(third_party_gateway)
    adapter.pay(200)

if __name__ == "__main__":
    main()