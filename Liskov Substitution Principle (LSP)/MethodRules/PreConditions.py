# A precondition must be satisfied before a method can be executed.
# Subclasses can weaken the precondition but cannot strengthen it.


class User:
    # Precondition: Password must be at least 8 characters long.
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long!")

        print("Password set successfully")


class AdminUser(User):
    # Precondition: Password must be at least 6 characters.
    def set_password(self, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long!")

        print("Password set successfully")


def main():
    user = AdminUser()   # Can also be treated as a User
    user.set_password("Admin123")   # Works fine: AdminUser allows shorter passwords


if __name__ == "__main__":
    main()