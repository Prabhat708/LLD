'''A drawing application receives a shape type at runtime and creates Circle, Rectangle or Triangle.'''

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def createShape(self):
        pass

class Circle(Shape):
    def createShape(self):
        return "Cricle is created"

class Rectangle(Shape):
    def createShape(self):
        return "Rectangle is created"

class Triangle(Shape):
    def createShape(self):
        return "Triangle is created"

class ShapeFactory:
    @staticmethod
    def ShapeType(type):
        if type=="circle":
            return Circle()
        elif type=="rectangle":
            return Rectangle()
        elif type=="triangle":
            return Triangle()
        else:
            return "This type is not supported"

if __name__== "__main__":
    shape=ShapeFactory.ShapeType("triangle")
    print(shape.createShape())

