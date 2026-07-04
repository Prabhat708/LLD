
class MenuItem():
      
    def __init__(self, code: str, name: str, price: float):
        self.code = code
        self.name = name
        self.price = price
        self.description = ""

    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
    def get_description(self):
        return self.description
    
    def get_code(self):
        return self.code
    
    def set_name(self, name: str):
        self.name = name

    def set_price(self, price: float):
        self.price = price

    def set_description(self, description: str):
        self.description = description
