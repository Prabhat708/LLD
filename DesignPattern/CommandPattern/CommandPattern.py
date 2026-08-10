from abc import ABC, abstractmethod


# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# Receivers
class Light:
    def on(self):
        print("Light is ON")

    def off(self):
        print("Light is OFF")


class Fan:
    def on(self):
        print("Fan is ON")

    def off(self):
        print("Fan is OFF")


# Concrete Command for Light
class LightCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


# Concrete Command for Fan
class FanCommand(Command):
    def __init__(self, fan):
        self.fan = fan

    def execute(self):
        self.fan.on()

    def undo(self):
        self.fan.off()


# Invoker: Remote Controller with static 2D array of 4 buttons
class RemoteController:
    NUM_BUTTONS = 4

    def __init__(self):
        self.buttons = [None] * self.NUM_BUTTONS
        self.button_pressed = [False] * self.NUM_BUTTONS
        # false = off, true = on

    def set_command(self, idx, command):
        if 0 <= idx < self.NUM_BUTTONS:
            self.buttons[idx] = command
            self.button_pressed[idx] = False

    def press_button(self, idx):
        if (
            0 <= idx < self.NUM_BUTTONS
            and self.buttons[idx] is not None
        ):
            if self.button_pressed[idx] is False:
                self.buttons[idx].execute()
            else:
                self.buttons[idx].undo()

            self.button_pressed[idx] = not self.button_pressed[idx]

        else:
            print(f"No command assigned at button {idx}")


def main():

    light = Light()
    ceiling_fan = Fan()

    remote = RemoteController()

    remote.set_command(0, LightCommand(light))
    remote.set_command(1, FanCommand(ceiling_fan))

    # Simulate button presses (toggle behavior)
    print("--- Toggling Light Button 0 ---")
    remote.press_button(0)  # ON
    remote.press_button(0)  # OFF

    print("--- Toggling Fan Button 1 ---")
    remote.press_button(1)  # ON
    remote.press_button(1)  # OFF

    # Press unassigned button to show default message
    print("--- Pressing Unassigned Button 2 ---")
    remote.press_button(2)


if __name__ == "__main__":
    main()