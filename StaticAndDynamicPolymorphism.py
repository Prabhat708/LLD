from abc import ABC, abstractmethod


# Abstract Base Class
class Car(ABC):

    # Constructor
    def __init__(self, brand, model):
        self._brand = brand
        self._model = model
        self._is_engine_on = False
        self._current_speed = 0

    # Common method for all cars
    def start_engine(self):
        self._is_engine_on = True
        print(f"{self._brand} {self._model} : Engine started.")

    # Common method for all cars
    def stop_engine(self):
        self._is_engine_on = False
        self._current_speed = 0
        print(f"{self._brand} {self._model} : Engine turned off.")

    # Abstract methods
    @abstractmethod
    def accelerate(self, speed=20):
        pass

    @abstractmethod
    def brake(self):
        pass


# Manual Car
class ManualCar(Car):

    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._current_gear = 0

    # Specialized method
    def shift_gear(self, gear):
        self._current_gear = gear
        print(f"{self._brand} {self._model} : Shifted to gear {gear}")

    # Method overriding
    # Default parameter simulates method overloading
    def accelerate(self, speed=20):

        if not self._is_engine_on:
            print(f"{self._brand} {self._model} : Cannot accelerate! Engine is off.")
            return

        self._current_speed += speed

        print(f"{self._brand} {self._model} : Accelerating to {self._current_speed} km/h")

    # Method overriding
    def brake(self):

        self._current_speed -= 20

        if self._current_speed < 0:
            self._current_speed = 0

        print(f"{self._brand} {self._model} : Braking! Speed is now {self._current_speed} km/h")


# Electric Car
class ElectricCar(Car):

    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._battery_level = 100

    # Specialized method
    def charge_battery(self):
        self._battery_level = 100
        print(f"{self._brand} {self._model} : Battery fully charged!")

    # Method overriding
    def accelerate(self, speed=15):

        if not self._is_engine_on:
            print(f"{self._brand} {self._model} : Cannot accelerate! Engine is off.")
            return

        if self._battery_level <= 0:
            print(f"{self._brand} {self._model} : Battery dead! Cannot accelerate.")
            return

        self._battery_level -= 10
        self._current_speed += speed

        print(
            f"{self._brand} {self._model} : "
            f"Accelerating to {self._current_speed} km/h. "
            f"Battery at {self._battery_level}%."
        )

    # Method overriding
    def brake(self):

        self._current_speed -= 15

        if self._current_speed < 0:
            self._current_speed = 0

        print(
            f"{self._brand} {self._model} : "
            f"Regenerative braking! "
            f"Speed is now {self._current_speed} km/h. "
            f"Battery at {self._battery_level}%."
        )


# Main
if __name__ == "__main__":

    # Parent reference pointing to child object
    my_manual_car: Car = ManualCar("Ford", "Mustang")

    my_manual_car.start_engine()
    my_manual_car.accelerate()
    my_manual_car.accelerate()
    my_manual_car.brake()
    my_manual_car.stop_engine()

    print("-" * 30)

    my_electric_car: Car = ElectricCar("Tesla", "Model S")

    my_electric_car.start_engine()
    my_electric_car.accelerate()
    my_electric_car.accelerate()
    my_electric_car.brake()
    my_electric_car.stop_engine()