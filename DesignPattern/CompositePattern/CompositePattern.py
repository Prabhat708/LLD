from abc import ABC, abstractmethod


# Base interface for files and folders
class FileSystemItem(ABC):

    @abstractmethod
    def ls(self, indent=0):
        pass

    @abstractmethod
    def open_all(self, indent=0):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def cd(self, name):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def is_folder(self):
        pass


# Leaf: File
class File(FileSystemItem):

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def ls(self, indent=0):
        print(" " * indent + self.name)

    def open_all(self, indent=0):
        print(" " * indent + self.name)

    def get_size(self):
        return self.size

    def cd(self, name):
        return None

    def get_name(self):
        return self.name

    def is_folder(self):
        return False


class Folder(FileSystemItem):

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, item):
        self.children.append(item)

    def ls(self, indent=0):
        for child in self.children:
            if child.is_folder():
                print(" " * indent + "+ " + child.get_name())
            else:
                print(" " * indent + child.get_name())

    def open_all(self, indent=0):
        print(" " * indent + "+ " + self.name)

        for child in self.children:
            child.open_all(indent + 4)

    def get_size(self):
        total = 0

        for child in self.children:
            total += child.get_size()

        return total

    def cd(self, target):
        for child in self.children:
            if child.is_folder() and child.get_name() == target:
                return child

        # not found or not a folder
        return None

    def get_name(self):
        return self.name

    def is_folder(self):
        return True


def main():

    # Build file system
    root = Folder("root")

    root.add(File("file1.txt", 1))
    root.add(File("file2.txt", 1))

    docs = Folder("docs")
    docs.add(File("resume.pdf", 1))
    docs.add(File("notes.txt", 1))
    root.add(docs)

    images = Folder("images")
    images.add(File("photo.jpg", 1))
    root.add(images)

    root.ls()

    docs.ls()

    root.open_all()

    cwd = root.cd("docs")

    if cwd is not None:
        cwd.ls()
    else:
        print("\n Could not cd into docs \n")

    print(root.get_size())


if __name__ == "__main__":
    main()