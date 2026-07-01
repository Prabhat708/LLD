# Return Type Rule:
# Subtype overridden method return type should be either identical
# or narrower than the parent method's return type.
# This is also called return type covariance.
# Python doesn't enforce this at runtime, but we can express it using type hints.


class Animal:
    # Some common Animal methods
    pass


class Dog(Animal):
    # Additional Dog methods specific to Dogs.
    pass


class Parent:
    def get_animal(self) -> Animal:
        print("Parent : Returning Animal instance")
        return Animal()


class Child(Parent):
    # Can also have return type as Dog
    def get_animal(self) -> Dog:
        print("Child : Returning Dog instance")
        return Dog()


class Client:
    def __init__(self, parent: Parent):
        self.parent = parent

    def take_animal(self):
        self.parent.get_animal()


def main():
    parent = Parent()
    child = Child()

    client = Client(child)
    # client = Client(parent)

    client.take_animal()


if __name__ == "__main__":
    main()