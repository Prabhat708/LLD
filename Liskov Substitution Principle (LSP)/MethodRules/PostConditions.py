# A postcondition must be satisfied after a method is executed.
# Subclasses can strengthen the postcondition but cannot weaken it.


class Car:
    def __init__(self):
        self.speed = 0

    def accelerate(self):
        print("Accelerating")
        self.speed += 20

    # Postcondition: Speed must reduce after brake.
    def brake(self):
        print("Applying brakes")
        self.speed -= 20


# Subclass can strengthen postcondition - Does not violate LSP
class HybridCar(Car):
    def __init__(self):
        super().__init__()
        self.charge = 0

    # Postcondition: Speed must reduce after brake.
    # Postcondition: Charge must increase.
    def brake(self):
        print("Applying brakes")
        self.speed -= 20
        self.charge += 10


def main():
    hybrid_car = HybridCar()   # Can also be treated as a Car
    hybrid_car.brake()         # Works fine: HybridCar reduces speed and also increases charge.

    # Client feels no difference in substituting HybridCar in place of Car.


if __name__ == "__main__":
    main()