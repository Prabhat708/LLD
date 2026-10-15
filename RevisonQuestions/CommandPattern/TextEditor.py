from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass
    @abstractmethod
    def redo(self):
        pass

class InsertTextCommand(Command):
    def __init__(self, text_editor, text):
        self.text_editor = text_editor
        self.text = text

    def execute(self):
        self.text_editor.insert_text(self.text)

    def undo(self):
        self.text_editor.delete_text(len(self.text))

    def redo(self):
        self.text_editor.insert_text(self.text)

class DeleteTextCommand(Command):
    def __init__(self, text_editor, length):
        self.text_editor = text_editor
        self.length = length
        self.deleted_text = ""

    def execute(self):
        if self.length <= 0:
            self.deleted_text = ""
            return

        current_text = self.text_editor.get_text()
        actual_length = min(self.length, len(current_text))

        self.deleted_text = current_text[-actual_length:]
        self.text_editor.delete_text(actual_length)

    def undo(self):
        if self.deleted_text:
            self.text_editor.insert_text(self.deleted_text)

    def redo(self):
        if self.deleted_text:
            self.text_editor.delete_text(len(self.deleted_text))
        

class TextEditor:
    def __init__(self):
        self.text = ""

    def insert_text(self, text):
        self.text += text
        print(f"Inserted text: '{text}'. Current text: '{self.text}'")

    def delete_text(self, length):
        if length <= 0:
            return

        deleted_text = self.text[-length:]
        self.text = self.text[:-length]
        print(f"Deleted text: '{deleted_text}'. Current text: '{self.text}'")

    def get_text(self):
        return self.text

class TextEditorController:
    def __init__(self):
        self.history = []
        self.redo_stack = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

        # A new action invalidates the previous redo history.
        self.redo_stack.clear()

    def undo_last_command(self):
        if not self.history:
            print("No commands to undo.")
            return

        last_command = self.history.pop()
        last_command.undo()
        self.redo_stack.append(last_command)

    def redo_last_command(self):
        if not self.redo_stack:
            print("No commands to redo.")
            return

        last_command = self.redo_stack.pop()
        last_command.redo()
        self.history.append(last_command)

def main():
    text_editor = TextEditor()
    controller = TextEditorController()

    # Create command objects
    insert_command1 = InsertTextCommand(text_editor, "Hello, ")
    insert_command2 = InsertTextCommand(text_editor, "World!")
    delete_command = DeleteTextCommand(text_editor, 6)
    insert_command3 = InsertTextCommand(text_editor, "Python!")

    # Execute commands
    controller.execute_command(insert_command1)
    controller.execute_command(insert_command2)
    controller.undo_last_command()  # Undo last insertion
    controller.execute_command(delete_command)

    # Undo last command (deletion)
    controller.undo_last_command()
    # Redo last command (deletion)
    controller.redo_last_command()
    controller.execute_command(insert_command3)
    controller.redo_last_command()  # Attempt to redo when there's nothing to redo
    controller.undo_last_command()  # Undo last insertion

if __name__ == "__main__":
    main()