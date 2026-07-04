from .Cart import Cart


class User:
    def __init__(self, user_id, name, address):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.cart = Cart()

    def __del__(self):
        self.cart = None

    # Getters and Setters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_cart(self):
        return self.cart