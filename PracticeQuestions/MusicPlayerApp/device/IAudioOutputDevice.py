from abc import ABC, abstractmethod


class IAudioOutputDevice(ABC):
    @abstractmethod
    def play_audio(self, song):
        pass
