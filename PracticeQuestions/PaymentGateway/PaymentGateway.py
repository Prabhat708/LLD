import random
import time
from abc import ABC, abstractmethod


# ============================================================
# 1. Payment Request
# ============================================================

class PaymentRequest:

    def __init__(self, sender, receiver, amount, currency):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.currency = currency


# ============================================================
# 2. Banking System
#    Strategy for actual payment processing
# ============================================================

class BankingSystem(ABC):

    @abstractmethod
    def process_payment(self, amount):
        pass


class PaytmBankingSystem(BankingSystem):

    def process_payment(self, amount):
        print(f"[BankingSystem-Paytm] Processing payment of {amount}...")

        # Simulate 20% success
        return random.randint(0, 99) < 20


class RazorpayBankingSystem(BankingSystem):

    def process_payment(self, amount):
        print(f"[BankingSystem-Razorpay] Processing payment of {amount}...")

        # Simulate 90% success
        return random.randint(0, 99) < 90

class BhimBankingSystem(BankingSystem):

    def process_payment(self, amount):
        print(f"[BankingSystem-Bhim] Processing payment of {amount}...")

        # Simulate 70% success
        return random.randint(0, 99) < 70
# ============================================================
# 3. Payment Gateway
#    Template Method Pattern
# ============================================================

class PaymentGateway(ABC):

    def __init__(self):
        self.banking_system = None

    # Template Method
    def process_payment(self, request):

        if not self.validate_payment(request):
            print(
                f"[PaymentGateway] Validation failed for "
                f"{request.sender}."
            )
            return False

        if not self.initiate_payment(request):
            print(
                f"[PaymentGateway] Initiation failed for "
                f"{request.sender}."
            )
            return False

        if not self.confirm_payment(request):
            print(
                f"[PaymentGateway] Confirmation failed for "
                f"{request.sender}."
            )
            return False

        return True

    @abstractmethod
    def validate_payment(self, request):
        pass

    @abstractmethod
    def initiate_payment(self, request):
        pass

    @abstractmethod
    def confirm_payment(self, request):
        pass


# ============================================================
# 4. Paytm Gateway
# ============================================================

class PaytmGateway(PaymentGateway):

    def __init__(self):
        super().__init__()
        self.banking_system = PaytmBankingSystem()

    def validate_payment(self, request):

        print(
            f"[Paytm] Validating payment for "
            f"{request.sender}."
        )

        if request.amount <= 0 or request.currency != "INR":
            return False

        return True

    def initiate_payment(self, request):

        print(
            f"[Paytm] Initiating payment of "
            f"{request.amount} {request.currency} "
            f"for {request.sender}."
        )

        return self.banking_system.process_payment(
            request.amount
        )

    def confirm_payment(self, request):

        print(
            f"[Paytm] Confirming payment for "
            f"{request.sender}."
        )

        return True


# ============================================================
# 5. Razorpay Gateway
# ============================================================

class RazorpayGateway(PaymentGateway):

    def __init__(self):
        super().__init__()
        self.banking_system = RazorpayBankingSystem()

    def validate_payment(self, request):

        print(
            f"[Razorpay] Validating payment for "
            f"{request.sender}."
        )

        if request.amount <= 0:
            return False

        return True

    def initiate_payment(self, request):

        print(
            f"[Razorpay] Initiating payment of "
            f"{request.amount} {request.currency} "
            f"for {request.sender}."
        )

        return self.banking_system.process_payment(
            request.amount
        )

    def confirm_payment(self, request):

        print(
            f"[Razorpay] Confirming payment for "
            f"{request.sender}."
        )

        return True


# ============================================================
# 6. Payment Gateway Proxy
#    Proxy Pattern
#    Adds retry functionality
# ============================================================

class PaymentGatewayProxy(PaymentGateway):

    def __init__(self, gateway, max_retries):
        super().__init__()

        self.real_gateway = gateway
        self.retries = max_retries

    def process_payment(self, request):

        result = False

        for attempt in range(self.retries):

            if attempt > 0:
                print(
                    f"[Proxy] Retrying payment "
                    f"(attempt {attempt + 1}) "
                    f"for {request.sender}."
                )

            result = self.real_gateway.process_payment(
                request
            )

            if result:
                break

        if not result:
            print(
                f"[Proxy] Payment failed after "
                f"{self.retries} attempts "
                f"for {request.sender}."
            )

        return result

    # Delegate remaining operations to real gateway

    def validate_payment(self, request):
        return self.real_gateway.validate_payment(request)

    def initiate_payment(self, request):
        return self.real_gateway.initiate_payment(request)

    def confirm_payment(self, request):
        return self.real_gateway.confirm_payment(request)


# ============================================================
# 7. Gateway Factory
#    Singleton + Factory
# ============================================================

class GatewayFactory:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def get_gateway(self, gateway_type):

        if gateway_type == "PAYTM":

            payment_gateway = PaytmGateway()

            return PaymentGatewayProxy(
                payment_gateway,
               20
            )

        elif gateway_type == "RAZORPAY":

            payment_gateway = RazorpayGateway()

            return PaymentGatewayProxy(
                payment_gateway,
                1
            )

        else:
            raise ValueError("Invalid gateway type")


# ============================================================
# 8. Payment Service
#    Singleton
# ============================================================

class PaymentService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.gateway = None

        return cls._instance

    def set_gateway(self, gateway):

        self.gateway = gateway

    def process_payment(self, request):

        if self.gateway is None:

            print(
                "[PaymentService] "
                "No payment gateway selected."
            )

            return False

        return self.gateway.process_payment(request)


# ============================================================
# 9. Payment Controller
#    Singleton
# ============================================================

class PaymentController:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def handle_payment(self, gateway_type, request):

        # Get gateway from Factory
        payment_gateway = (
            GatewayFactory()
            .get_gateway(gateway_type)
        )

        # Set gateway in PaymentService
        PaymentService().set_gateway(
            payment_gateway
        )

        # Process payment
        return PaymentService().process_payment(
            request
        )


# ============================================================
# 10. Main
# ============================================================

if __name__ == "__main__":

    random.seed(time.time())

    # Payment Request 1

    req1 = PaymentRequest(
        "Aditya",
        "Shubham",
        1000.0,
        "INR"
    )

    print("Processing via Paytm")
    print("------------------------------")

    result1 = (
        PaymentController()
        .handle_payment(
            "PAYTM",
            req1
        )
    )

    print(
        "Result:",
        "SUCCESS" if result1 else "FAIL"
    )

    print("------------------------------\n")


    # Payment Request 2

    req2 = PaymentRequest(
        "Shubham",
        "Aditya",
        500.0,
        "USD"
    )

    print("Processing via Razorpay")
    print("------------------------------")

    result2 = (
        PaymentController()
        .handle_payment(
            "RAZORPAY",
            req2
        )
    )

    print(
        "Result:",
        "SUCCESS" if result2 else "FAIL"
    )

    print("------------------------------")