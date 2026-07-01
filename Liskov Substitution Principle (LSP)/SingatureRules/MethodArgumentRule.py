# Method Argument Rule:
# Subtype method arguments can be identical or wider than the supertype.
# Python doesn't enforce method signatures, but to follow LSP,
# the overridden method should accept at least what the parent accepts.


class Parent:
    def print(self, msg):
        print(f"Parent: {msg}")


class Child(Parent):
    def print(self, msg):
        print(f"Child: {msg}")


# Client that passes a string as msg, as the client expects.
class Client:
    def __init__(self, parent: Parent):
        self.parent = parent

    def print_msg(self):
        self.parent.print("Hello")


def main():
    parent = Parent()
    child = Child()

    client = Client(parent)
    # client = Client(child)

    client.print_msg()


if __name__ == "__main__":
    main()