from abc import ABC, abstractmethod

# Abstract Base Class
class OnlyDepositAccount(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass

class WithdrawableAccount(OnlyDepositAccount):
    @abstractmethod
    def withdraw(self, amount):
        pass

class SavingAccount(WithdrawableAccount):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Savings Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount} from Savings Account. New Balance: {self.balance}")
        else:
            print("Insufficient funds in Savings Account!")


class CurrentAccount(WithdrawableAccount):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Current Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount} from Current Account. New Balance: {self.balance}")
        else:
            print("Insufficient funds in Current Account!")

class FixedTermAccount(OnlyDepositAccount):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Fixed Term Account. New Balance: {self.balance}")

    # No withdraw method here, adhering to LSP  


class BankClient:
    def __init__(
        self,
        depositable_accounts: list[OnlyDepositAccount],
        withdraw_accounts: list[WithdrawableAccount]
    ):
        self.deposit_accounts = depositable_accounts
        self.withdraw_accounts = withdraw_accounts

    def process_transactions(self):
        print("---- Deposits ----")
        for account in self.deposit_accounts:
            account.deposit(1000)

        print("\n---- Withdrawals ----")
        for account in self.withdraw_accounts:
            account.withdraw(500)

def main():
    savings = SavingAccount()
    current = CurrentAccount()
    fixed = FixedTermAccount()

    deposit_accounts = [
        savings,
        current,
        fixed
    ]

    withdraw_accounts = [
        savings,
        current
    ]

    client = BankClient(deposit_accounts, withdraw_accounts)
    client.process_transactions()


if __name__ == "__main__":
    main()