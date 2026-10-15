from abc import ABC, abstractmethod

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

  

class WithdrawCommand(Command):
    def __init__(self, atm_machine, amount):
        self.atm_machine = atm_machine
        self.amount = amount

    def execute(self):
        if self.atm_machine.get_balance() >= self.amount:
            self.atm_machine.withdraw(self.amount)
            print(f"Withdrew Rs.{self.amount}. New balance: Rs.{self.atm_machine.get_balance()}.")
        else:
            print("Insufficient funds for withdrawal.")
    

class DepositCommand(Command):
    def __init__(self, atm_machine, amount):
        self.atm_machine = atm_machine
        self.amount = amount

    def execute(self):
        self.atm_machine.deposit(self.amount)
        print(f"Deposited Rs.{self.amount}. New balance: Rs.{self.atm_machine.get_balance()}.")

    
class CheckBalanceCommand(Command):
    def __init__(self, atm_machine):
        self.atm_machine = atm_machine

    def execute(self):
        print(f"Current balance: Rs.{self.atm_machine.get_balance()}.")

class ATMMachine:
    def __init__(self):
        self.balance = 0

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

    
class ATMController:
    def execute_command(self, command):
        command.execute()
def main():
    atm_machine = ATMMachine()
    controller = ATMController()
    # Create command objects
    
    deposit_command = DepositCommand(atm_machine, 100)
    withdraw_command = WithdrawCommand(atm_machine, 1000)
    check_balance_command = CheckBalanceCommand(atm_machine)

    # Execute commands
    controller.execute_command(check_balance_command)
    controller.execute_command(deposit_command)
    controller.execute_command(check_balance_command)
    controller.execute_command(withdraw_command)
    controller.execute_command(check_balance_command)

if __name__ == "__main__":
    main()