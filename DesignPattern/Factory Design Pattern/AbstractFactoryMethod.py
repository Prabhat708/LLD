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
    
class GarlicBread(ABC):
    @abstractmethod
    def prepare(self):
        pass

class RegularGarlicBread(GarlicBread):
    def prepare(self):
        return "Preparing Regular Garlic Bread with lettuce, tomato, and cheese."

class WheatGarlicBread(GarlicBread):
    def prepare(self):
        return "Preparing Wheat Garlic Bread with whole wheat bun, lettuce, tomato, and cheese."

class CheeseGarlicBread(GarlicBread):
    def prepare(self):
        return "Preparing Cheese Garlic Bread with extra cheese and special sauce."
    
class CheeseWheatGarlicBread(GarlicBread):
    def prepare(self):
        return "Preparing Cheese Wheat Garlic Bread with whole wheat bun, extra cheese, and special sauce."
    
class MealFactory(ABC):
    @abstractmethod
    def create_buger(self, buger_type):
        pass

    @abstractmethod
    def create_garlic_bread(self, garlic_bread_type):
        pass

class RegularMealFactory(MealFactory):
    def create_buger(self, buger_type):
        if buger_type == "basic":
            return BasicBuger()
        elif buger_type == "cheese":
            return CheeseBuger()
        elif buger_type == "premium":
            return PremiumBuger()
        else:
            raise ValueError("Invalid buger type. Please choose 'basic', 'cheese', or 'premium'.")

    def create_garlic_bread(self, garlic_bread_type):
        if garlic_bread_type == "regular":
            return RegularGarlicBread()
        elif garlic_bread_type == "wheat":
            return WheatGarlicBread()
        elif garlic_bread_type == "cheese":
            return CheeseGarlicBread()
        elif garlic_bread_type == "cheese_wheat":
            return CheeseWheatGarlicBread()
        else:
            raise ValueError("Invalid garlic bread type. Please choose 'regular', 'wheat', 'cheese', or 'cheese_wheat'.")
        
class WheatMealFactory(MealFactory):
    def create_buger(self, buger_type):
        if buger_type == "basic":
            return BasicwheatBuger()
        elif buger_type == "cheese":
            return CheesewheatBuger()
        elif buger_type == "premium":
            return PremiumwheatBuger()
        else:
            raise ValueError("Invalid buger type. Please choose 'basic', 'cheese', or 'premium'.")

    def create_garlic_bread(self, garlic_bread_type):
        if garlic_bread_type == "regular":
            return RegularGarlicBread()
        elif garlic_bread_type == "wheat":
            return WheatGarlicBread()
        elif garlic_bread_type == "cheese":
            return CheeseGarlicBread()
        elif garlic_bread_type == "cheese_wheat":
            return CheeseWheatGarlicBread()
        else:
            raise ValueError("Invalid garlic bread type. Please choose 'regular', 'wheat', 'cheese', or 'cheese_wheat'.")
         
def main():
    buger_type = input("Enter the type of buger (basic, cheese, premium): ").lower()
    try:
        factory_type = input("Enter the factory type (regular, wheat): ").lower()
        if factory_type == "regular":
            factory = RegularMealFactory()
        elif factory_type == "wheat":
            factory = WheatMealFactory()
        else:
            raise ValueError("Invalid factory type. Please choose 'regular' or 'wheat'.")
        
        buger = factory.create_buger(buger_type)
        garlic_bread_type = input("Enter the type of garlic bread (regular, wheat, cheese, cheese_wheat): ").lower()
        garlic_bread = factory.create_garlic_bread(garlic_bread_type)
        print(buger.prepare())
        print(garlic_bread.prepare())
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()