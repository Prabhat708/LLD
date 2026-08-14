from abc import ABC, abstractmethod


# Product
class Transportation(ABC):

    @abstractmethod
    def deliver(self):
        pass


# Concrete Products
class Truck(Transportation):

    def deliver(self):
        return "Delivering goods by road with trucks."


class Ship(Transportation):

    def deliver(self):
        return "Delivering goods by sea with ships."


# Creator
class Logistics(ABC):

    @abstractmethod
    def create_transportation(self):
        pass

    def plan_delivery(self):
        transportation = self.create_transportation()
        return transportation.deliver()


# Concrete Creators
class RoadLogistics(Logistics):

    def create_transportation(self):
        return Truck()


class SeaLogistics(Logistics):

    def create_transportation(self):
        return Ship()


if __name__ == "__main__":

    logistics_type = input("Enter logistics type (road/sea): ").lower()

    if logistics_type == "road":
        logistics = RoadLogistics()

    elif logistics_type == "sea":
        logistics = SeaLogistics()

    else:
        raise ValueError("Invalid logistics type.")

    print(logistics.plan_delivery())