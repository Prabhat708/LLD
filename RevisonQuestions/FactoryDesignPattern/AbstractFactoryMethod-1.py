from abc import ABC, abstractmethod


# Abstract Product: Button
class Button(ABC):
    @abstractmethod
    def create_button(self):
        pass


# Abstract Product: Checkbox
class Checkbox(ABC):
    @abstractmethod
    def create_checkbox(self):
        pass


# Concrete Products: Windows
class WindowsButton(Button):
    def create_button(self):
        return "Windows button clicked"


class WindowsCheckbox(Checkbox):
    def create_checkbox(self):
        return "Windows checkbox created"


# Concrete Products: Mac
class MacButton(Button):
    def create_button(self):
        return "Mac button clicked"


class MacCheckbox(Checkbox):
    def create_checkbox(self):
        return "Mac checkbox created"


# Concrete Products: Linux
class LinuxButton(Button):
    def create_button(self):
        return "Linux button clicked"


class LinuxCheckbox(Checkbox):
    def create_checkbox(self):
        return "Linux checkbox created"


# Abstract Factory
class GuiFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass


# Concrete Factory: Windows
class WindowsFactory(GuiFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()


# Concrete Factory: Mac
class MacFactory(GuiFactory):
    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()


# Concrete Factory: Linux
class LinuxFactory(GuiFactory):
    def create_button(self):
        return LinuxButton()

    def create_checkbox(self):
        return LinuxCheckbox()


# Client
class Application:
    def __init__(self, factory: GuiFactory):
        self.factory = factory

    def create_ui(self):
        button = self.factory.create_button()
        checkbox = self.factory.create_checkbox()

        print(button.create_button())
        print(checkbox.create_checkbox())


if __name__ == "__main__":

    factory_type = input(
        "Enter the factory type (windows, mac, linux): "
    ).lower()

    if factory_type == "windows":
        factory = WindowsFactory()

    elif factory_type == "mac":
        factory = MacFactory()

    elif factory_type == "linux":
        factory = LinuxFactory()

    else:
        raise ValueError(
            "Invalid factory type. Please choose 'windows', 'mac', or 'linux'."
        )

    app = Application(factory)
    app.create_ui()