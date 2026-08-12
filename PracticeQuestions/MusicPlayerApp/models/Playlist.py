from models.Song import Song


class Playlist:
    def __init__(self, name):
        self.playlist_name = name
        self.song_list = []

    def get_playlist_name(self):
        return self.playlist_name

    def get_songs(self):
        return self.song_list

    def get_size(self):
        return len(self.song_list)

    def add_song_to_playlist(self, song):
        if song is None:
            raise RuntimeError("Cannot add null song to playlist.")
        self.song_list.append(song)
