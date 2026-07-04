class OrderManager:
    _instance = None

    def __init__(self):
        # Private Constructor
        self.orders = []

    @staticmethod
    def get_instance():
        if OrderManager._instance is None:
            OrderManager._instance = OrderManager()
        return OrderManager._instance

    def add_order(self, order):
        self.orders.append(order)

    def list_orders(self):
        print("\n--- All Orders ---")
        for order in self.orders:
            print(
                f"{order.get_type()} order for {order.get_user().get_name()} "
                f"| Total: ₹{order.get_total()} "
                f"| At: {order.get_scheduled()}"
            )