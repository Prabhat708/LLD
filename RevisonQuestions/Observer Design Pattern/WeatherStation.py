from abc import ABC, abstractmethod

class IDisplayElement(ABC):
    @abstractmethod
    def display(self):
        pass

class IStation(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

class WeatherStation(IStation):
    def __init__(self,name):
        self.name = name
        self.observers = []
        self.temperature = 0.0
        self.humidity = 0.0

    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature, self.humidity)

    def set_measurements(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity
        self.notify_observers()

    def get_measurements(self):
        return self.temperature, self.humidity

class DisplayElement(IDisplayElement):
    def __init__(self,name, station):
        self.name = name
        self.station = station

    def update(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity
        self.display()

    def display(self):
        print(
            f"{self.name} Display - "
            f"Temperature: {self.temperature}°C, "
            f"Humidity: {self.humidity}%"
        )

def main():
    station = WeatherStation("Main Station")

    display1 = DisplayElement("PhoneDisplay", station)
    display2 = DisplayElement("DesktopDisplay", station)
    display3 = DisplayElement("TabletDisplay", station)

    station.register_observer(display1)
    station.register_observer(display2)
    station.register_observer(display3)

    station.set_measurements(25.0, 60.0)
    print("\nRemoving DesktopDisplay observer...\n")
    station.remove_observer(display2)
    station.set_measurements(30.0, 55.0)
if __name__ == "__main__":
    main()
