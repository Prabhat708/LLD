# Subclass methods should not allow state changes that
# the base class never allowed.


class BankAccount:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("Balance can't be negative")
        self.balance = balance

    # History Constraint: Withdraw should be allowed.
    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise RuntimeError("Insufficient funds")

        self.balance -= amount
        print(f"Amount withdrawn. Remaining balance is {self.balance}")


class FixedDepositAccount(BankAccount):
    def __init__(self, balance):
        super().__init__(balance)

    # LSP break! History Constraint broke!
    # Parent class behaviour changed: Now withdraw is not allowed.
    # This class will break client code that relies on withdraw.
    def withdraw(self, amount):
        raise RuntimeError("Withdraw not allowed in Fixed Deposit")


def main():
    bank_account = BankAccount(100)
    # bank_account = FixedDepositAccount(100)

    bank_account.withdraw(100)


if __name__ == "__main__":
    main()