from core.AudioEngine import AudioEngine
from managers.DeviceManager import DeviceManager
from managers.PlaylistManager import PlaylistManager
from managers.StrategyManager import StrategyManager


class MusicPlayerFacade:
    _instance = None

    def __init__(self):
        self.loaded_playlist = None
        self.play_strategy = None
        self.audio_engine = AudioEngine()

    @staticmethod
    def get_instance():
        if MusicPlayerFacade._instance is None:
            MusicPlayerFacade._instance = MusicPlayerFacade()
        return MusicPlayerFacade._instance

    def connect_device(self, device_type):
        DeviceManager.get_instance().connect(device_type)

    def set_play_strategy(self, strategy_type):
        self.play_strategy = StrategyManager.get_instance().get_strategy(strategy_type)

    def load_playlist(self, name):
        self.loaded_playlist = PlaylistManager.get_instance().get_playlist(name)
        if self.play_strategy is None:
            raise RuntimeError("Play strategy not set before loading.")
        self.play_strategy.set_playlist(self.loaded_playlist)

    def play_song(self, song):
        if not DeviceManager.get_instance().has_output_device():
            raise RuntimeError("No audio device connected.")
        device = DeviceManager.get_instance().get_output_device()
        self.audio_engine.play(device, song)

    def pause_song(self, song):
        if self.audio_engine.get_current_song_title() != song.get_title():
            raise RuntimeError(
                f'Cannot pause "{song.get_title()}"; not currently playing.'
            )
        self.audio_engine.pause()

    def play_all_tracks(self):
        if self.loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        while self.play_strategy.has_next():
            next_song = self.play_strategy.next()
            device = DeviceManager.get_instance().get_output_device()
            self.audio_engine.play(device, next_song)

        print(f"Completed playlist: {self.loaded_playlist.get_playlist_name()}")

    def play_next_track(self):
        if self.loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        if self.play_strategy.has_next():
            next_song = self.play_strategy.next()
            device = DeviceManager.get_instance().get_output_device()
            self.audio_engine.play(device, next_song)
        else:
            print(f"Completed playlist: {self.loaded_playlist.get_playlist_name()}")

    def play_previous_track(self):
        if self.loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        if self.play_strategy.has_previous():
            previous_song = self.play_strategy.previous()
            device = DeviceManager.get_instance().get_output_device()
            self.audio_engine.play(device, previous_song)
        else:
            print(f"Completed playlist: {self.loaded_playlist.get_playlist_name()}")

    def enqueue_next(self, song):
        self.play_strategy.add_to_next(song)
