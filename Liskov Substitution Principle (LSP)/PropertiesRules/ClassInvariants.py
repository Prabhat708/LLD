# Class Invariant:
# A child class should not break the invariants (guarantees) of the parent class.
# Hence, a child class can maintain or strengthen the invariant,
# but it should never weaken it.

# Invariant: Balance cannot be negative.


class BankAccount:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("Balance can't be negative")
        self.balance = balance

    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise RuntimeError("Insufficient funds")

        self.balance -= amount
        print(f"Amount withdrawn. Remaining balance is {self.balance}")


# Breaks invariant: Should not be allowed.
class CheatAccount(BankAccount):
    def __init__(self, balance):
        super().__init__(balance)

    def withdraw(self, amount):
        self.balance -= amount      # LSP break! Negative balance allowed
        print(f"Amount withdrawn. Remaining balance is {self.balance}")


def main():
    # bank_account = BankAccount(100)
    bank_account = CheatAccount(100)

    bank_account.withdraw(200)


if __name__ == "__main__":
    main()