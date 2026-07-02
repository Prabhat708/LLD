from abc import ABC, abstractmethod

# Abstract Base Class
class TwoDShape(ABC):
    @abstractmethod
    def area(self):
        pass

class ThreeDShape(ABC):
    @abstractmethod
    def volume(self):
        pass

    @abstractmethod
    def area(self):
        pass

class Square(TwoDShape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Cube(ThreeDShape):
    def __init__(self, side):
        self.side = side

    def volume(self):
        return self.side ** 3

    def area(self):
        return 6 * (self.side ** 2)
    

def main():
    square = Square(4)
    print(f"Area of square: {square.area()}")

    cube = Cube(3)
    print(f"Area of cube: {cube.area()}")
    print(f"Volume of cube: {cube.volume()}")

if __name__ == "__main__":
    main()

