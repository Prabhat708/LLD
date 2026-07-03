class Singleton:
    _instance = None

    def __init__(self):
        print("Singleton Constructor Called!")

    @staticmethod
    def get_instance():
        return Singleton._instance


# Initialize static member (Eager Initialization)
Singleton._instance = Singleton()


def main():
    s1 = Singleton.get_instance()
    s2 = Singleton.get_instance()

    print(s1 is s2)


if __name__ == "__main__":
    main()