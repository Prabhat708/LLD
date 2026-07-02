from abc import ABC, abstractmethod
# Abstract Base Class

class shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def volume(self):
        pass


class Square(shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def volume(self):
        raise NotImplementedError("Volume is not applicable for a square.")
    

class Cube(shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return 6 * (self.side ** 2)

    def volume(self):
        return self.side ** 3
    
def main():
    square = Square(4)
    print(f"Area of square: {square.area()}")
    try:
        print(f"Volume of square: {square.volume()}") #ISP breached, as volume is not applicable for square
    except NotImplementedError as e:
        print(e)

    cube = Cube(3)
    print(f"Area of cube: {cube.area()}")
    print(f"Volume of cube: {cube.volume()}")

if __name__ == "__main__":
    main()