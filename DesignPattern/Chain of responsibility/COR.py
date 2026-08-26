from abc import ABC, abstractmethod


# Abstract Handler
class MoneyHandler(ABC):

    def __init__(self):
        self.next_handler = None

    def set_next_handler(self, next_handler):
        self.next_handler = next_handler

    @abstractmethod
    def dispense(self, amount):
        pass


# Concrete Handler: ₹1000
class ThousandHandler(MoneyHandler):

    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 1000

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹1000 notes.")

        remaining_amount = amount - (notes_needed * 1000)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )


# Concrete Handler: ₹500
class FiveHundredHandler(MoneyHandler):

    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 500

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹500 notes.")

        remaining_amount = amount - (notes_needed * 500)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )


# Concrete Handler: ₹200
class TwoHundredHandler(MoneyHandler):

    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 200

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹200 notes.")

        remaining_amount = amount - (notes_needed * 200)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )


# Concrete Handler: ₹100
class HundredHandler(MoneyHandler):

    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 100

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹100 notes.")

        remaining_amount = amount - (notes_needed * 100)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )

class FiftyHandler(MoneyHandler):

    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 50

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹50 notes.")

        remaining_amount = amount - (notes_needed * 50)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )
class TwentyHandler(MoneyHandler):

    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 20

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹20 notes.")

        remaining_amount = amount - (notes_needed * 20)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )
class TenHandler(MoneyHandler):
    
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):

        notes_needed = amount // 10

        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹10 notes.")

        remaining_amount = amount - (notes_needed * 10)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled (Insufficient fund in ATM)"
                )
# Client
if __name__ == "__main__":

    # Create handlers
    thousand_handler = ThousandHandler(3)
    five_hundred_handler = FiveHundredHandler(5)
    two_hundred_handler = TwoHundredHandler(10)
    hundred_handler = HundredHandler(20)
    fifty_handler = FiftyHandler(40)
    twenty_handler = TwentyHandler(20)
    ten_handler = TenHandler(200)
    # Create the chain
    thousand_handler.set_next_handler(five_hundred_handler)
    five_hundred_handler.set_next_handler(two_hundred_handler)
    two_hundred_handler.set_next_handler(hundred_handler)
    hundred_handler.set_next_handler(fifty_handler)
    fifty_handler.set_next_handler(twenty_handler)
    twenty_handler.set_next_handler(ten_handler)

    amount_to_withdraw = int(input("Enter the amount to withdraw: ₹"))
    if amount_to_withdraw <= 0:
        print("Please enter a valid amount greater than zero.")
    elif amount_to_withdraw % 10 != 0:
        print("Please enter an amount that is a multiple of ₹10.")
        
    else:
        thousand_handler.dispense(amount_to_withdraw)
