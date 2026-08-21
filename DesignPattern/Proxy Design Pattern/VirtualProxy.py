from abc import ABC, abstractmethod


# Interface
class IImage(ABC):

    @abstractmethod
    def display(self):
        pass


# Real Object
class RealImage(IImage):

    def __init__(self, filename):
        self.filename = filename

        # Heavy operation
        print(
            f"[RealImage] Loading image from disk: {self.filename}"
        )

    def display(self):
        print(
            f"[RealImage] Displaying {self.filename}"
        )


# Virtual Proxy
class ImageProxy(IImage):

    def __init__(self, filename):
        self.filename = filename
        self.real_image = None

    def display(self):

        # Lazy initialization
        if self.real_image is None:
            self.real_image = RealImage(self.filename)

        self.real_image.display()


# Client
if __name__ == "__main__":

    image1 = ImageProxy("sample.jpg")

    image1.display()