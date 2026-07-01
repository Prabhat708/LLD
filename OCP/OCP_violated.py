class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products
    
    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product.price
        return total
    
class InvoicePrinter:
    def print_invoice(self, cart):
        print("Shopping Cart Invoice:")
        for product in cart.get_products():
            print(f"{product.name} - Rs {product.price}")
        print(f"Total: Rs {cart.calculate_total()}")

class DatabaseSaver:
    def saveToSql(self, cart):
        print("Saving shopping cart to SQL database...")

    def saveToMongo(self, cart):
        print("Saving shopping cart to MongoDB...")

    def saveToFile(self, cart):
        print("Saving shopping cart to file...")

def main():
    cart = ShoppingCart()

    cart.add_product(Product("Laptop", 50000))
    cart.add_product(Product("Mouse", 2000))

    invoice_printer = InvoicePrinter()
    invoice_printer.print_invoice(cart)

    database_saver = DatabaseSaver()
    database_saver.saveToSql(cart)
    database_saver.saveToMongo(cart)
    database_saver.saveToFile(cart)

if __name__ == "__main__":
    main()