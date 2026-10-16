from abc import ABC, abstractmethod

class InventoryService:
    def __init__(self):
        self.inventory = {}

    def add_product(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id] += quantity
        else:
            self.inventory[product_id] = quantity

    def remove_product(self, product_id, quantity):
        if product_id in self.inventory and self.inventory[product_id] >= quantity:
            self.inventory[product_id] -= quantity
            return True
        return False

    def check_availability(self, product_id):
        return self.inventory.get(product_id, 0) > 0

class PaymentService:
    def process_payment(self, amount):
        print(f"Processing payment of Rs. {amount}...")
        # Simulate payment processing logic
        return True

class ShippingService:
    def ship_product(self, product_id):
        print(f"Shipping product {product_id}...")
        # Simulate shipping logic
        return True

class NotificationService:
    def send_notification(self, message):
        print(f"Sending notification: {message}")

class PlaceOrderFacade:
    def __init__(self):
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
        self.shipping_service = ShippingService()
        self.notification_service = NotificationService()

    def place_order(self, product_id, quantity, amount):
        if not self.inventory_service.check_availability(product_id):
            print(f"Product {product_id} is out of stock.")
            return False

        if not self.inventory_service.remove_product(product_id, quantity):
            print(f"Failed to remove product {product_id} from inventory.")
            return False

        if not self.payment_service.process_payment(amount):
            print("Payment failed.")
            return False

        if not self.shipping_service.ship_product(product_id):
            print(f"Failed to ship product {product_id}.")
            return False

        self.notification_service.send_notification(f"Order placed for product {product_id}.")
        print("Order placed successfully!")
        return True

def main():
    facade = PlaceOrderFacade()
    # Adding some products to inventory for testing
    facade.inventory_service.add_product("P001", 10)
    facade.inventory_service.add_product("P002", 5)

    # Placing an order
    product_id = "P001"
    quantity = 2
    amount = 500
    facade.place_order(product_id, quantity, amount)

if __name__ == "__main__":
    main()