from abc import ABC, abstractmethod

class Walkable(ABC):
    @abstractmethod
    def walk(self):
        pass

class NormalWalk(Walkable):
    def walk(self):
        print("Walking Normally...")

class NoWalk(Walkable):
    def walk(self):
        print("Not Walking...")


class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass

class NormalFly(Flyable):
    def fly(self):
        print("Flying Normally...")
        
class NoFly(Flyable):
    def fly(self):
        print("Not Flying...")


class Talkable(ABC):
    @abstractmethod
    def talk(self):
        pass

class NormalTalk(Talkable):
    def talk(self):
        print("Talking Normally...")

class NoTalk(Talkable):
    def talk(self):
        print("Not Talking...")


class Robot(ABC):
    def __init__(self, walkable, flyable, talkable):
        self.walkable = walkable
        self.flyable = flyable
        self.talkable = talkable

    def walk(self):
        self.walkable.walk()

    def fly(self):
        self.flyable.fly()

    def talk(self):
        self.talkable.talk()

    @abstractmethod
    def projection(self):
        pass
class companionRobot(Robot):
    def projection(self):
        print("Projecting a holographic companion...")
class WorkerRobot(Robot):
    def projection(self):
        print("Projecting work-related information...")

def main():
    # Create a robot that can walk, fly, talk, and project a companion
    companion_robot = companionRobot(NormalWalk(), NoFly(), NormalTalk())
    print("Companion Robot:")
    companion_robot.walk()
    companion_robot.fly()
    companion_robot.talk()
    companion_robot.projection()

    print("-"*50)
    # Create a robot that can walk, talk, and project work-related information but cannot fly
    worker_robot = WorkerRobot(NormalWalk(), NoFly(), NormalTalk())
    print("Worker Robot:")
    worker_robot.walk()
    worker_robot.fly()  # This will indicate that the robot cannot fly
    worker_robot.talk()
    worker_robot.projection()

if __name__ == "__main__":
    main()



