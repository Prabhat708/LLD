from abc import ABC, abstractmethod

# Abstract Base Class
class Buger(ABC):
    @abstractmethod
    def prepare(self):
        pass

class BasicBuger(Buger):
    def prepare(self):
        return "Preparing Basic Buger with lettuce, tomato, and cheese."
    
class CheeseBuger(Buger):
    def prepare(self):
        return "Preparing Cheese Buger with extra cheese and special sauce."
    
class PremiumBuger(Buger):
    def prepare(self):
        return "Preparing Premium Buger with premium ingredients and gourmet toppings."
    
class BasicwheatBuger(Buger):
    def prepare(self):
        return "Preparing Basic Wheat Buger with whole wheat bun, lettuce, tomato, and cheese."

class CheesewheatBuger(Buger):
    def prepare(self):
        return "Preparing Cheese Wheat Buger with whole wheat bun, extra cheese, and special sauce."
    
class PremiumwheatBuger(Buger):
    def prepare(self):
        return "Preparing Premium Wheat Buger with whole wheat bun, premium ingredients, and gourmet toppings."
    

    
class BugerFactory(ABC):
    @abstractmethod
    def create_buger(self, buger_type):
        pass

class RegularBugerFactory(BugerFactory):
    def create_buger(self, buger_type):
        if buger_type == "basic":
            return BasicBuger()
        elif buger_type == "cheese":
            return CheeseBuger()
        elif buger_type == "premium":
            return PremiumBuger()
        else:
            raise ValueError("Invalid buger type. Please choose 'basic', 'cheese', or 'premium'.")
        
class WheatBugerFactory(BugerFactory):
    def create_buger(self, buger_type):
        if buger_type == "basic":
            return BasicwheatBuger()
        elif buger_type == "cheese":
            return CheesewheatBuger()
        elif buger_type == "premium":
            return PremiumwheatBuger()
        else:
            raise ValueError("Invalid buger type. Please choose 'basic', 'cheese', or 'premium'.")
         
def main():
    buger_type = input("Enter the type of buger (basic, cheese, premium): ").lower()
    try:
        factory_type = input("Enter the factory type (regular, wheat): ").lower()
        if factory_type == "regular":
            factory = RegularBugerFactory()
        elif factory_type == "wheat":
            factory = WheatBugerFactory()
        else:
            raise ValueError("Invalid factory type. Please choose 'regular' or 'wheat'.")
        
        buger = factory.create_buger(buger_type)
        print(buger.prepare())
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()