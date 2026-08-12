from models.Playlist import Playlist


class PlaylistManager:
    _instance = None

    def __init__(self):
        self.playlists = {}

    @staticmethod
    def get_instance():
        if PlaylistManager._instance is None:
            PlaylistManager._instance = PlaylistManager()
        return PlaylistManager._instance

    def create_playlist(self, name):
        if name in self.playlists:
            raise RuntimeError(f'Playlist "{name}" already exists.')
        self.playlists[name] = Playlist(name)

    def add_song_to_playlist(self, playlist_name, song):
        if playlist_name not in self.playlists:
            raise RuntimeError(f'Playlist "{playlist_name}" not found.')
        self.playlists[playlist_name].add_song_to_playlist(song)

    def get_playlist(self, name):
        if name not in self.playlists:
            raise RuntimeError(f'Playlist "{name}" not found.')
        return self.playlists[name]
