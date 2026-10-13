from abc import ABC, abstractmethod

class Coffie(ABC):

    @abstractmethod
    def getCoffie(self):
        pass
    @abstractmethod
    def getCost(self):
        pass

class BasicCoffie(Coffie):

    def getCoffie(self):
        return "Basic Coffie"
    def getCost(self):
        return 100

class CoffieDecorator(Coffie):

    def __init__(self, coffie):
        self.coffie = coffie

class MilkDecorator(CoffieDecorator):

    def getCoffie(self):
        return self.coffie.getCoffie() + " with Milk"
    def getCost(self):
        return self.coffie.getCost() + 20

class CaramelDecorator(CoffieDecorator):

    def getCoffie(self):
        return self.coffie.getCoffie() + " with Caramel"
    def getCost(self):
        return self.coffie.getCost() + 30

class ExtraEspressoDecorator(CoffieDecorator):

    def getCoffie(self):
        return self.coffie.getCoffie() + " with Extra Espresso"
    def getCost(self):
        return self.coffie.getCost() + 40

class ChocolateDecorator(CoffieDecorator):

    def getCoffie(self):
        return self.coffie.getCoffie() + " with Chocolate"
    def getCost(self):
        return self.coffie.getCost() + 50

def main():
    basic_coffie = BasicCoffie()
    coffee = ExtraEspressoDecorator(basic_coffie)
    coffee = MilkDecorator(coffee)
    coffee = CaramelDecorator(coffee)
    coffee = ChocolateDecorator(coffee)

    print(coffee.getCoffie())
    print(coffee.getCost())

    

if __name__ == "__main__":
    main()

    