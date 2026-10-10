
from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


# =========================================================
# 1. DISCOUNT STRATEGIES
# =========================================================

class DiscountStrategy(ABC):

    @abstractmethod
    def calculate_discount(self, amount):
        pass


class FlatDiscount(DiscountStrategy):

    def __init__(self, discount_amount):
        if discount_amount < 0:
            raise ValueError("Discount cannot be negative")
        self.discount_amount = discount_amount

    def calculate_discount(self, amount):
        return min(amount, self.discount_amount)


class PercentageDiscount(DiscountStrategy):

    def __init__(self, discount_percentage):
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        self.discount_percentage = discount_percentage

    def calculate_discount(self, amount):
        return amount * self.discount_percentage / 100


class PercentageDiscountWithCap(PercentageDiscount):

    def __init__(self, discount_percentage, cap_amount):
        super().__init__(discount_percentage)
        if cap_amount < 0:
            raise ValueError("Cap cannot be negative")
        self.cap_amount = cap_amount

    def calculate_discount(self, amount):
        return min(
            amount,
            super().calculate_discount(amount),
            self.cap_amount
        )


class StrategyType(Enum):
    FLAT = 1
    PERCENTAGE = 2
    PERCENTAGE_WITH_CAP = 3


# =========================================================
# 2. PRODUCT, USER AND CART ITEM
# =========================================================

class Product:

    def __init__(self, product_id, name, price, category_id):
        if price < 0:
            raise ValueError("Product price cannot be negative")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.category_id = category_id


class User:

    def __init__(self, user_id, name, loyalty_points=0):
        if loyalty_points < 0:
            raise ValueError("Loyalty points cannot be negative")

        self.user_id = user_id
        self.name = name
        self.loyalty_points = loyalty_points


class CartItem:

    def __init__(self, product, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.product = product
        self.quantity = quantity

    def calculate_total(self):
        return self.product.price * self.quantity


# =========================================================
# 3. CART CONTEXT
# =========================================================

class Cart:

    def __init__(self, user):
        self.user = user
        self.items = []
        self.applied_coupons = []

    def add_product(self, product, quantity=1):
        self.items.append(CartItem(product, quantity))

    def calculate_total(self):
        return sum(item.calculate_total() for item in self.items)

    def calculate_total_after_coupons(self):
        total = self.calculate_total()

        for coupon in self.applied_coupons:
            total -= coupon.calculate_discount(
                coupon.get_eligible_amount(self),
                max_discount=total
            )

        return max(0, round(total, 2))


# =========================================================
# 4. COUPON RULES
# =========================================================

class CouponRule(ABC):

    @abstractmethod
    def is_valid(self, cart, context):
        pass

    def filter_items(self, items):
        # By default, a coupon applies to all cart items.
        return items


class MinimumAmountRule(CouponRule):

    def __init__(self, minimum_amount):
        if minimum_amount < 0:
            raise ValueError("Minimum amount cannot be negative")
        self.minimum_amount = minimum_amount

    def is_valid(self, cart, context):
        return cart.calculate_total() >= self.minimum_amount


class DateRangeRule(CouponRule):

    def __init__(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError("Start date must not exceed end date")

        self.start_date = start_date
        self.end_date = end_date

    def is_valid(self, cart, context):
        current_date = context.get("current_date", date.today())

        return self.start_date <= current_date <= self.end_date


class UserRule(CouponRule):

    def __init__(self, user_id):
        self.user_id = user_id

    def is_valid(self, cart, context):
        return cart.user.user_id == self.user_id


class BankingSystemRule(CouponRule):

    def __init__(self, bank_name):
        self.bank_name = bank_name

    def is_valid(self, cart, context):
        return context.get("banking_system") == self.bank_name


class LoyaltyPointsRule(CouponRule):

    def __init__(self, required_points):
        if required_points < 0:
            raise ValueError("Required points cannot be negative")
        self.required_points = required_points

    def is_valid(self, cart, context):
        return cart.user.loyalty_points >= self.required_points


class ProductRule(CouponRule):

    def __init__(self, product_id):
        self.product_id = product_id

    def is_valid(self, cart, context):
        return any(
            item.product.product_id == self.product_id
            for item in cart.items
        )

    def filter_items(self, items):
        return [
            item for item in items
            if item.product.product_id == self.product_id
        ]


class CategoryRule(CouponRule):

    def __init__(self, category_id):
        self.category_id = category_id

    def is_valid(self, cart, context):
        return any(
            item.product.category_id == self.category_id
            for item in cart.items
        )

    def filter_items(self, items):
        return [
            item for item in items
            if item.product.category_id == self.category_id
        ]


# =========================================================
# 5. COUPON
# =========================================================

class DiscountCoupon:

    def __init__(
        self,
        code,
        strategy,
        rules=None,
        combinable=True
    ):
        self.code = code
        self.strategy = strategy
        self.rules = rules or []
        self.combinable = combinable

    def is_valid(self, cart, context=None):
        context = context or {}

        return all(
            rule.is_valid(cart, context)
            for rule in self.rules
        )

    def get_eligible_amount(self, cart):
        eligible_items = cart.items

        # All item filters are combined using intersection.
        for rule in self.rules:
            eligible_items = rule.filter_items(eligible_items)

        return sum(
            item.calculate_total()
            for item in eligible_items
        )

    def calculate_discount(self, amount, max_discount=None):
        discount = self.strategy.calculate_discount(amount)

        if max_discount is not None:
            discount = min(discount, max_discount)

        return round(max(0, discount), 2)


# =========================================================
# 6. COUPON MANAGER
# =========================================================

class DiscountCouponManager:

    def __init__(self):
        self.coupons = {}

    def add_coupon(self, coupon):
        if coupon.code in self.coupons:
            raise ValueError(f"Duplicate coupon code: {coupon.code}")

        self.coupons[coupon.code] = coupon

    def get_coupon(self, code):
        return self.coupons.get(code)


# =========================================================
# 7. COUPON SERVICE
# =========================================================

class CouponService:

    def __init__(self, coupon_manager):
        self.coupon_manager = coupon_manager

    def apply_coupon(self, cart, coupon_code, context=None):
        context = context or {}
        coupon = self.coupon_manager.get_coupon(coupon_code)

        if coupon is None:
            return {
                "success": False,
                "message": "Invalid coupon code",
                "total": cart.calculate_total_after_coupons()
            }

        if any(c.code == coupon_code for c in cart.applied_coupons):
            return {
                "success": False,
                "message": "Coupon already applied",
                "total": cart.calculate_total_after_coupons()
            }

        if not coupon.is_valid(cart, context):
            return {
                "success": False,
                "message": "Coupon conditions are not satisfied",
                "total": cart.calculate_total_after_coupons()
            }

        if cart.applied_coupons and (
            not coupon.combinable
            or any(not c.combinable for c in cart.applied_coupons)
        ):
            return {
                "success": False,
                "message": "Coupon cannot be combined",
                "total": cart.calculate_total_after_coupons()
            }

        cart.applied_coupons.append(coupon)

        return {
            "success": True,
            "message": f"Coupon {coupon_code} applied successfully",
            "total": cart.calculate_total_after_coupons()
        }


# =========================================================
# 8. DEMO
# =========================================================

def main():
    coupon_manager = DiscountCouponManager()

    # Flat discount: Rs. 50 off on orders of Rs. 200+
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="FLAT50",
            strategy=FlatDiscount(50),
            rules=[MinimumAmountRule(200)]
        )
    )

    # Bank offer: 10% off for BOB customers on orders of Rs. 100+
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="BOB10",
            strategy=PercentageDiscount(10),
            rules=[
                MinimumAmountRule(100),
                BankingSystemRule("BOB")
            ]
        )
    )

    # 50% off, capped at Rs. 100; cannot be combined
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="UPTO100",
            strategy=PercentageDiscountWithCap(50, 100),
            rules=[MinimumAmountRule(300)],
            combinable=False
        )
    )

    # 20% off a particular product
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="PRODUCT20",
            strategy=PercentageDiscount(20),
            rules=[ProductRule(101)]
        )
    )

    # 15% off a particular category
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="CATEGORY15",
            strategy=PercentageDiscount(15),
            rules=[CategoryRule(2)]
        )
    )

    # Seasonal offer
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="FESTIVE",
            strategy=PercentageDiscount(25),
            rules=[
                MinimumAmountRule(200),
                DateRangeRule(
                    date(2026, 10, 1),
                    date(2026, 10, 31)
                )
            ]
        )
    )

    # User-specific offer
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="USER50",
            strategy=FlatDiscount(50),
            rules=[UserRule(1)]
        )
    )

    # Loyalty offer
    coupon_manager.add_coupon(
        DiscountCoupon(
            code="LOYALTY",
            strategy=FlatDiscount(100),
            rules=[LoyaltyPointsRule(100)]
        )
    )

    user = User(1, "John Doe", loyalty_points=150)

    cart = Cart(user)

    cart.add_product(
        Product(101, "Keyboard", 500, 1),
        quantity=2
    )
    cart.add_product(
        Product(102, "Mouse", 250, 2),
        quantity=1
    )

    service = CouponService(coupon_manager)

    print("Subtotal:", cart.calculate_total())
    result = service.apply_coupon(
            cart,
            "UPTO100",
            context={"banking_system": "BOB"}
        )
    print(result["message"])
    result = service.apply_coupon(
        cart,
        "LOYALTY",
        context={
            "current_date": date.today(),
            "banking_system": "BOB"
        }
    )
    print(result["message"])
    result = service.apply_coupon(
        cart,
        "USER50",   
    )
    print(result["message"])
    
    # This will be rejected because UPTO100 is non-combinable.
    result = service.apply_coupon(
        cart,
        "BOB10",
        context={"banking_system": "BOB"}
    )
    
    print(result["message"])
    
    print("Final payable:", result["total"])


if __name__ == "__main__":
    main()
