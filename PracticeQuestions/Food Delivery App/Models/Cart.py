class Cart:
    def __init__(self):
        self.restaurant = None
        self.items = []

    def add_item(self, item):
        if self.restaurant is None:
            print("Cart: Set a restaurant before adding items.")
            return

        self.items.append(item)

    def get_total_cost(self):
        total = 0

        for item in self.items:
            total += item.get_price()

        return total

    def is_empty(self):
        return self.restaurant is None or len(self.items) == 0

    def clear(self):
        self.items.clear()
        self.restaurant = None

    # Getters and Setters
    def set_restaurant(self, restaurant):
        self.restaurant = restaurant

    def get_restaurant(self):
        return self.restaurant

    def get_items(self):
        return self.items