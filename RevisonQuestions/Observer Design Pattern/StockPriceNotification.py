from abc import ABC, abstractmethod

class IInvestor(ABC):
    @abstractmethod
    def update(self, stock_price, stock_name):
        pass

class IStock(ABC):
    @abstractmethod
    def register_investor(self, investor):
        pass

    @abstractmethod
    def remove_investor(self, investor):
        pass

    @abstractmethod
    def notify_investors(self):
        pass

class Stock(IStock):
    def __init__(self, name):
        self.name = name
        self.investors = []
        self.stock_price = 0.0

    def register_investor(self, investor):
        if investor not in self.investors:
            self.investors.append(investor)

    def remove_investor(self, investor):
        if investor in self.investors:
            self.investors.remove(investor)

    def notify_investors(self):
        for investor in self.investors:
            investor.update(self.stock_price, self.name)

    def set_stock_price(self, stock_price):
        self.stock_price = stock_price
        self.notify_investors()

    def get_stock_price(self):
        return self.stock_price

class Investor(IInvestor):
    def __init__(self, name):
        self.name = name
       

    def update(self, stock_price, stock_name):
        self.stock_price = stock_price
        self.stock_name = stock_name
        self.display()

    def display(self):
        print(
            f"{self.name} Investor - Stock: {self.stock_name},   Price: {self.stock_price}"
        )

def main():
    stock = Stock("TCS")
    stock2 = Stock("Infosys")
    rahul = Investor("Rahul")
    amit = Investor("Amit")
    sarah = Investor("Sarah")

    stock.register_investor(rahul)
    stock.register_investor(amit)
    stock2.register_investor(sarah)
    stock2.register_investor(rahul)
    stock.set_stock_price(3500)
    stock2.set_stock_price(1500)
    print("\nRemoving Amit from the investor list...\n")
    stock.remove_investor(amit)
    stock.set_stock_price(3600) 
    stock2.set_stock_price(1600)

if __name__ == "__main__":
    main()