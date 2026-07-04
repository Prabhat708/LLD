from .Order import Order
class DeliveryOrder(Order):
    def __init__(self):
        super().__init__()
        self.user_address = ""

    def get_type(self):
        return "Delivery"

    # Getters and Setters
    def set_user_address(self, address):
        self.user_address = address

    def get_user_address(self):
        return self.user_address