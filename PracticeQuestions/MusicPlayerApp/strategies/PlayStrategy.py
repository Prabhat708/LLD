from abc import ABC, abstractmethod


class PlayStrategy(ABC):
    @abstractmethod
    def set_playlist(self, playlist):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def previous(self):
        pass

    @abstractmethod
    def has_previous(self):
        pass

    def add_to_next(self, song):
        pass
