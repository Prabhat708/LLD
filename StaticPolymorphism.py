class Car:
  
    # Constructor - Automatically called whenever a new SportsCar object is created.
    def __init__(self, brand, model):

        # Protected attributes (accessible, but intended for internal use)
        self._IsEngineOn = False
        self._currentGear = 0

        # Private attribute (name mangled by Python)
        # Should only be accessed through class methods.
        self.__CurrentSpeed = 0

        # Public attributes
        self.Brand = brand
        self.Model = model


    # Getter - Provides read-only access to the private speed variable.
    def getSpped(self):
        return self.__CurrentSpeed

    # Starts the engine.
    def start_engine(self):
        self._IsEngineOn = True
        print(f"{self.Brand} {self.Model} Engine Started with a roar!")

    # Changes the gear only if the engine is running.
    def gearShift(self, gear):

        if self._IsEngineOn:
            self._currentGear = gear
            print(f"{self.Brand} {self.Model} shifted to gear {gear}.")
        else:
            print(f"Cannot shift gears. {self.Brand} {self.Model} engine is off.")

  
    def accelerate(self, speed=20):
        if self._IsEngineOn:
            self.__CurrentSpeed += speed
            print(f"{self.Brand} {self.Model} is accelerating. Current speed: {self.__CurrentSpeed} km/h.")
        else:
            print(f"Cannot accelerate. {self.Brand} {self.Model} engine is off.")
            
    # Decreases the speed by 20 km/h.
    # Speed is never allowed to become negative.
    def brake(self):

        if self._IsEngineOn:
            self.__CurrentSpeed -= 20

        if self.__CurrentSpeed < 0:
            self.__CurrentSpeed = 0

        print(f"{self.Brand} {self.Model} is braking. Current speed: {self.__CurrentSpeed} km/h.")

    # Stops the engine and resets the car's state.
    def stop_engine(self):

        self._IsEngineOn = False
        self.__CurrentSpeed = 0
        self._currentGear = 0

        print(f"{self.Brand} {self.Model} Engine Stopped.")


# Entry point of the program.
# Code inside this block executes only when this file is run directly.
if __name__ == "__main__":

    # Create a SportsCar object.
    my_car = Car("Ferrari", "488 Spider")

    # Perform various car operations.
    my_car.start_engine()
    my_car.gearShift(1)
    my_car.accelerate()
    my_car.gearShift(2)
    my_car.accelerate(30)  # Accelerate by 30 km/h using the overloaded method
    my_car.brake()
    my_car.stop_engine()

