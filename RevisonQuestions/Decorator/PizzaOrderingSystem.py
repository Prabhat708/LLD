from abc import ABC, abstractmethod

class Pizza(ABC):

    @abstractmethod
    def getDescription(self):
        pass

    @abstractmethod
    def getCost(self):
        pass

class BasicPizza(Pizza):

    def getDescription(self):
        return "Basic Pizza"

    def getCost(self):
        return 200

class PizzaDecorator(Pizza):

    def __init__(self, pizza):
        self.pizza = pizza  

class CheeseDecorator(PizzaDecorator):

    def getDescription(self):
        return self.pizza.getDescription() + " with Cheese"

    def getCost(self):
        return self.pizza.getCost() + 50

class OlivesDecorator(PizzaDecorator):

    def getDescription(self):
        return self.pizza.getDescription() + " with Olives"

    def getCost(self):
        return self.pizza.getCost() + 30

class MushroomDecorator(PizzaDecorator):

    def getDescription(self):
        return self.pizza.getDescription() + " with Mushroom"

    def getCost(self):
        return self.pizza.getCost() + 40

class ExtraCheeseDecorator(PizzaDecorator):

    def getDescription(self):
        return self.pizza.getDescription() + " with Extra Cheese"

    def getCost(self):
        return self.pizza.getCost() + 60

def main():
    basic_pizza = BasicPizza()
    pizza = CheeseDecorator(basic_pizza)
    pizza = OlivesDecorator(pizza)
    pizza = MushroomDecorator(pizza)
    pizza = ExtraCheeseDecorator(pizza)
    pizza = CheeseDecorator(pizza)  # Adding extra cheese again

    print(pizza.getDescription())
    print(pizza.getCost())

if __name__ == "__main__":
    main()