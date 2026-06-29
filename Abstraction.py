from abc import ABC, abstractmethod

# Abstract Base Class (Blueprint)
# Defines WHAT a car can do but not HOW it does it.
# Any class inheriting from Car must implement all these methods.
class Car(ABC):
    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def stop_engine(self):
        pass

    @abstractmethod
    def gearShift(self, gear):
        pass

    @abstractmethod
    def accelerate(self):
        pass
    @abstractmethod
    def brake(self):
        pass

# Concrete Class
# Implements all the abstract methods defined in Car.
class SportsCar(Car):

     # Constructor - Called automatically when an object is created.
    def __init__(self,brand, model):
         # Initial state of the car
        self.IsEngineOn = False
        self.currentGear = 0
        self.CurrentSpeed = 0
         # Store the brand and model of the car
        self.Brand = brand
        self.Model = model
     # Implementation of abstract method

    def start_engine(self):
        self.IsEngineOn = True
        print(f"{self.Brand} {self.Model} Engine Started with a roar!")

    def gearShift(self, gear):
        if self.IsEngineOn:
            self.currentGear = gear
            print(f"{self.Brand} {self.Model} shifted to gear {gear}.")
        else:
            print(f"Cannot shift gears. {self.Brand} {self.Model} engine is off.")
    
    def accelerate(self):
        if self.IsEngineOn:
            self.CurrentSpeed += 20
            print(f"{self.Brand} {self.Model} is accelerating. Current speed: {self.CurrentSpeed} km/h.")
        else:
            print(f"Cannot accelerate. {self.Brand} {self.Model} engine is off.")
    
    def brake(self):
        if self.IsEngineOn:
            self.CurrentSpeed -=20
        if self.CurrentSpeed < 0:
            self.CurrentSpeed = 0
        print(f"{self.Brand} {self.Model} is braking. Current speed: {self.CurrentSpeed} km/h.")
    def stop_engine(self):
        self.IsEngineOn = False
        self.CurrentSpeed = 0
        self.currentGear = 0
        print(f"{self.Brand} {self.Model} Engine Stopped.")


# Entry point of the program
# Code inside this block executes only when this file is run directly.
if __name__ == "__main__":

    # Runtime Polymorphism:
    # Parent reference pointing to a Child object.
    # Type hint (: Car) is optional and helps IDEs understand the variable type.
    my_car:Car = SportsCar("Ferrari", "488 Spider")
    my_car.start_engine()
    my_car.gearShift(1)
    my_car.accelerate()
    my_car.accelerate()
    my_car.brake()
    my_car.stop_engine()