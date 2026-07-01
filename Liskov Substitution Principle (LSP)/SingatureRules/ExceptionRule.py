# Parent Exception
class ParentException(Exception):
    pass


# Child Exception (Narrower Exception)
class ChildException(ParentException):
    pass


# Exception Rule:
# A subclass should throw fewer or narrower exceptions
# (but not additional or broader exceptions) than the parent.
# Python does not enforce this. Hence no compilation/runtime check.

'''
Exception
├── ParentException
│   └── ChildException
│
└── RuntimeError
'''

# (The above hierarchy is for understanding.)

class Parent:
    def get_value(self):
        # Parent throws ParentException
        raise ParentException("Parent error")


class Child(Parent):
    def get_value(self):
        # Child throws ChildException
        raise ChildException("Child error")

        # raise RuntimeError("Child Error")  # This is Wrong


class Client:
    def __init__(self, parent):
        self.parent = parent

    def take_value(self):
        try:
            self.parent.get_value()
        except ParentException as e:
            print(f"Parent exception occurred: {e}")


def main():
    parent = Parent()
    child = Child()

    client = Client(child)  # Parent reference pointing to child object
    # client = Client(child)

    client.take_value()


if __name__ == "__main__":
    main()