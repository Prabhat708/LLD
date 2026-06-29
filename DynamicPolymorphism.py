from abc import ABC, abstractmethod
class Car(ABC):
    

    # Constructor - Automatically called whenever a new Car object is created.
    def __init__(self, brand, model):

        # Protected attributes (accessible, but intended for internal use)
        self._IsEngineOn = False
        self._CurrentSpeed = 0

        # Public attributes
        self.Brand = brand
        self.Model = model

 
    # Starts the engine.
    def start_engine(self):
        self._IsEngineOn = True
        print(f"{self.Brand} {self.Model} Engine Started with a roar!")

    @abstractmethod
    def accelerate(self):
        pass
    @abstractmethod
    def brake(self):
        pass

    # Stops the engine and resets the car's state.
    def stop_engine(self):

        self._IsEngineOn = False
        self._CurrentSpeed = 0
        self._currentGear = 0

        print(f"{self.Brand} {self.Model} Engine Stopped.")

class ManualCar(Car):
    def __init__(self,brand, model):
        super().__init__(brand, model)
        self._currentGear = 0


    def gearShift(self, gear):
        if self._IsEngineOn:
            self._currentGear = gear
            print(f"{self.Brand} {self.Model} shifted to gear {gear}.")
        else:
            print(f"Cannot shift gears. {self.Brand} {self.Model} engine is off.")
    def accelerate(self):

        if self._IsEngineOn:
            self._CurrentSpeed += 20
            print(f"{self.Brand} {self.Model} is accelerating. Current speed: {self._CurrentSpeed} km/h.")
        else:
            print(f"Cannot accelerate. {self.Brand} {self.Model} engine is off.")

    def brake(self):
        if self._IsEngineOn:
            self._CurrentSpeed -= 20

        if self._CurrentSpeed < 0:
            self._CurrentSpeed = 0

        print(f"{self.Brand} {self.Model} is braking. Current speed: {self._CurrentSpeed} km/h.")

class ElectricCar(Car):
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self.batteryPercentage = 100
    def chargeBattery(self, percentage):
        if 0 <= percentage <= 100:
            self.batteryPercentage = percentage
            print(f"{self.Brand} {self.Model} battery charged to {percentage}%.")
        else:
            print("Invalid battery percentage. Must be between 0 and 100.")
    
    def accelerate(self):
        if self._IsEngineOn:
            self.batteryPercentage -= 5  # Decrease battery percentage by 5% for each acceleration
            self._CurrentSpeed += 15
            print(f"{self.Brand} {self.Model} is accelerating. Current speed: {self._CurrentSpeed} km/h.")
        else:
            print(f"Cannot accelerate. {self.Brand} {self.Model} engine is off.")
    
    def brake(self):
        if self._IsEngineOn:
            self._CurrentSpeed -= 15
        if self._CurrentSpeed < 0:
            self._CurrentSpeed = 0
        print(f"{self.Brand} {self.Model} is braking. Current speed: {self._CurrentSpeed} km/h.")

# Entry point of the program.
# Code inside this block executes only when this file is run directly.
if __name__ == "__main__":
    # Create a ManualCar object.
    my_manual_car = ManualCar("Toyota", "Corolla")
    my_manual_car.start_engine()
    my_manual_car.gearShift(1) # Specific to ManualCar
    my_manual_car.accelerate()
    my_manual_car.brake()
    my_manual_car.stop_engine()


    print("\n--- Electric Car Operations ---\n")
    # Create an ElectricCar object.
    my_electric_car = ElectricCar("Tesla", "Model S")
    my_electric_car.start_engine()
    my_electric_car.accelerate()
    my_electric_car.chargeBattery(80) # Specific to ElectricCar
    my_electric_car.brake()
    my_electric_car.stop_engine()