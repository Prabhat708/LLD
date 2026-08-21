# Interface for Document Reader
from abc import ABC, abstractmethod


class IDocumentReader(ABC):

    @abstractmethod
    def unlock_pdf(self, file_path, password):
        pass


# Real Object
class RealDocumentReader(IDocumentReader):

    def unlock_pdf(self, file_path, password):
        print(f"[RealDocumentReader] Unlocking PDF at: {file_path}")
        print(
            f"[RealDocumentReader] PDF unlocked successfully "
            f"with password: {password}"
        )
        print("[RealDocumentReader] Displaying PDF content...")


# User class
class User:

    def __init__(self, name, is_premium):
        self.name = name
        self.premium_membership = is_premium


# Proxy
class DocumentProxy(IDocumentReader):

    def __init__(self, user):
        self.real_reader = RealDocumentReader()
        self.user = user

    def unlock_pdf(self, file_path, password):

        # Protection Proxy
        if not self.user.premium_membership:
            print(
                "[DocumentProxy] Access denied. "
                "Only premium members can unlock PDFs."
            )
            return

        # Forward request to real object
        self.real_reader.unlock_pdf(file_path, password)


# Client
if __name__ == "__main__":

    user1 = User("Rohan", False)
    user2 = User("Rashmi", True)

    print("== Rohan (Non-Premium) tries to unlock PDF ==")

    doc_reader = DocumentProxy(user1)

    doc_reader.unlock_pdf(
        "protected_document.pdf",
        "secret123"
    )

    print("\n== Rashmi (Premium) unlocks PDF ==")

    doc_reader = DocumentProxy(user2)

    doc_reader.unlock_pdf(
        "protected_document.pdf",
        "secret123"
    )