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
    
class BugerFactory:
    @staticmethod
    def create_buger(buger_type):
        if buger_type == "basic":
            return BasicBuger()
        elif buger_type == "cheese":
            return CheeseBuger()
        elif buger_type == "premium":
            return PremiumBuger()
        else:
            raise ValueError("Invalid buger type. Please choose 'basic', 'cheese', or 'premium'.")
        
def main():
    buger_type = input("Enter the type of buger (basic, cheese, premium): ").lower()
    try:
        buger = BugerFactory.create_buger(buger_type)
        print(buger.prepare())
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()