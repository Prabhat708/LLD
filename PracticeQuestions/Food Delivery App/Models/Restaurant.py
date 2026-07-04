class Restaurant:
    next_restaurant_id = 0

    def __init__(self, name, location):
        self.name = name
        self.location = location

        Restaurant.next_restaurant_id += 1
        self.restaurant_id = Restaurant.next_restaurant_id

        self.menu = []

    def __del__(self):
        # Optional: just for clarity or debug
        print(f"Destroying Restaurant: {self.name}, and clearing its menu.")
        self.menu.clear()

    # Getters and setters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def add_menu_item(self, item):
        self.menu.append(item)

    def get_menu(self):
        return self.menu