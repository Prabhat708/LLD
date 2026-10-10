from abc import ABC, abstractmethod

class Engine(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class PetrolEngine(Engine):

    def start(self):
        print("Starting petrol engine...")

    def stop(self):
        print("Stopping petrol engine...")

class DieselEngine(Engine):

    def start(self):
        print("Starting diesel engine...")

    def stop(self):
        print("Stopping diesel engine...")
class ElectricEngine(Engine):

    def start(self):
        print("Starting electric engine...")

    def stop(self):
        print("Stopping electric engine...")

class Car(ABC):

    def __init__(self, engine: Engine):
        self.engine = engine

    @abstractmethod
    def drive(self):
        pass

class SUV(Car):

    def drive(self):
        print("Driving an SUV...")
        self.engine.start()
        print("SUV is moving.")
        self.engine.stop()
class Sedan(Car):

    def drive(self):
        print("Driving a Sedan...")
        self.engine.start()
        print("Sedan is moving.")
        self.engine.stop()

class Hatchback(Car):

    def drive(self):
        print("Driving a Hatchback...")
        self.engine.start()
        print("Hatchback is moving.")
        self.engine.stop()
class Thar(Car):

    def drive(self):
        print("Driving a Thar...")
        self.engine.start()
        print("Thar is moving.")
        self.engine.stop()

def main():
    petrol_engine = PetrolEngine()
    diesel_engine = DieselEngine()
    electric_engine = ElectricEngine()

    suv = SUV(petrol_engine)
    sedan = Sedan(diesel_engine)
    hatchback = Hatchback(electric_engine)
    thar = Thar(petrol_engine)

    suv.drive()
    print()
    sedan.drive()
    print()
    hatchback.drive()
    print()
    thar.drive()

if __name__ == "__main__":
    main()