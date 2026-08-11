# Subsystems
class PowerSupply:
    def provide_power(self):
        print("Power Supply: Providing power...")


class CoolingSystem:
    def start_fans(self):
        print("Cooling System: Fans started...")


class CPU:
    def initialize(self):
        print("CPU: Initialization started...")


class Memory:
    def self_test(self):
        print("Memory: Self-test passed...")


class HardDrive:
    def spin_up(self):
        print("Hard Drive: Spinning up...")


class BIOS:
    def boot(self, cpu, memory):
        print("BIOS: Booting CPU and Memory checks...")
        cpu.initialize()
        memory.self_test()


class OperatingSystem:
    def load(self):
        print("Operating System: Loading into memory...")


# Facade
class ComputerFacade:
    def __init__(self):
        self.power_supply = PowerSupply()
        self.cooling_system = CoolingSystem()
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
        self.bios = BIOS()
        self.os = OperatingSystem()

    def start_computer(self):
        print("----- Starting Computer -----")

        self.power_supply.provide_power()
        self.cooling_system.start_fans()
        self.bios.boot(self.cpu, self.memory)
        self.hard_drive.spin_up()
        self.os.load()

        print("Computer Booted Successfully!")


# Client
def main():
    computer = ComputerFacade()
    computer.start_computer()


if __name__ == "__main__":
    main()