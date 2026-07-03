from threading import Lock


class Singleton:
    __instance = None
    __lock = Lock()

    def __init__(self):
        print("Singleton Constructor Called!")

    # Double check locking..
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:  # First check (no locking)
            with cls.__lock:  # Lock only if needed
                if cls.__instance is None:  # Second check (after acquiring lock)
                    cls.__instance = cls()
        return cls.__instance


def main():
    s1 = Singleton.get_instance()
    s2 = Singleton.get_instance()

    print(s1 is s2)


if __name__ == "__main__":
    main()