class SportsCar:
    """
    SportsCar class demonstrating Encapsulation in Python.

    Encapsulation means:
    1. Bundling data (attributes) and methods (functions) into a single class.
    2. Restricting direct access to sensitive data using naming conventions
       (_protected and __private) and exposing controlled access through
       getters and setters.
    """

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

        # Default tyre company
        self._tyre = "MRF"

    # Getter - Provides read-only access to the private speed variable.
    def getSpped(self):
        return self.__CurrentSpeed

    # Getter - Returns the current tyre company.
    def getTyre(self):
        return self._tyre

    # Setter - Updates the tyre company after validating the input.
    def setTyre(self, tyre):

        # Allow only approved tyre brands.
        if tyre in ["MRF", "JK", "Apollo"]:
            self._tyre = tyre
        else:
            print(f"{tyre} tyre brand is not allowed in this car.")

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

    # Increases the car's speed by 20 km/h.
    def accelerate(self):

        if self._IsEngineOn:
            self.__CurrentSpeed += 20
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
    my_car = SportsCar("Ferrari", "488 Spider")

    # Perform various car operations.
    my_car.start_engine()
    my_car.gearShift(1)
    my_car.accelerate()
    my_car.gearShift(2)
    my_car.accelerate()
    my_car.brake()
    my_car.stop_engine()

    # Direct access to private variables is discouraged.
    # This creates a new attribute instead of modifying the actual private variable.
    # my_car.__CurrentSpeed = 500

    # Access the private variable using its getter.
    print(my_car.getSpped())

    # Get the current tyre company.
    print(my_car.getTyre())

    # Update tyre company using the setter.
    my_car.setTyre("Apollo")
    print(my_car.getTyre())

    # Invalid tyre company (validation will fail).
    my_car.setTyre("Bridgestone")
    print(my_car.getTyre())