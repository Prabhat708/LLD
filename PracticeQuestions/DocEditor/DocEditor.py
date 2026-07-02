from abc import ABC, abstractmethod

# Abstract Base Class
class DocumentElement(ABC):
    @abstractmethod
    def render(self):
        pass

class Text(DocumentElement):
    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content
    
class Image(DocumentElement):
    def __init__(self, image_path):
        self.image_path = image_path

    def render(self):
        return f"Image: {self.image_path}"

class Document:
    def __init__(self):
        self.elements = []

    def add_element(self, element: DocumentElement):
        self.elements.append(element)

    def getElements(self):
        return self.elements
    
class DocumentRenderer:
    def render_document(self, document: Document):
        for element in document.getElements():
            print(element.render())

class Persistance(ABC):
    @abstractmethod
    def save(self, document: Document):
        pass

    @abstractmethod
    def load(self, file_path: str):
        pass

class FilePersistance(Persistance):
    def save(self, document: Document):
        open("document.txt", "w").write("\n".join([element.render() for element in document.getElements()]))
        print("Document saved to file.")


    def load(self, file_path: str):
        content = open(file_path, "r").read()
        print("Document loaded from file.")
        return content

class DatabasePersistance(Persistance):
    def save(self, document: Document):
        # Simulate saving to a database
        print("Document saved to database.")

    def load(self, file_path: str):
        # Simulate loading from a database
        print("Document loaded from database.")
        return "Database content"
    
class DocumentEditor:
    def __init__(self, document: Document):
        self.document = document
       
    def add_text(self, content):
        self.document.add_element(Text(content))

    def add_image(self, image_path):
        self.document.add_element(Image(image_path))

    def add_newline(self):
        self.document.add_element(Text("\n"))
    
    def add_bold_text(self, content):
        self.document.add_element(Text(f"**{content}**"))

    def add_tab(self):
        self.document.add_element(Text("\t"))

def main():
    document = Document()
    editor = DocumentEditor(document)

    editor.add_text("Hello, World!")
    editor.add_image("image.png")
    editor.add_newline()
    editor.add_tab()
    editor.add_bold_text("This is bold text.")
    editor.add_newline()
    editor.add_text("Another line.")


    renderer = DocumentRenderer()
    renderer.render_document(document)

    file_persistance = FilePersistance()
    file_persistance.save(document)
    file_persistance.load("document.txt")

    db_persistance = DatabasePersistance()
    db_persistance.save(document)
    db_persistance.load("database_path")

if __name__ == "__main__":
    main()

    