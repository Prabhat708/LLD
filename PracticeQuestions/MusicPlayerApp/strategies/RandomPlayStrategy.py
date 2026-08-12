import random

from strategies.PlayStrategy import PlayStrategy


class RandomPlayStrategy(PlayStrategy):
    def __init__(self):
        self.current_playlist = None
        self.remaining_songs = []
        self.history = []

    def set_playlist(self, playlist):
        self.current_playlist = playlist
        if not self.current_playlist or self.current_playlist.get_size() == 0:
            return

        self.remaining_songs = list(self.current_playlist.get_songs())
        self.history = []

    def has_next(self):
        return self.current_playlist is not None and bool(self.remaining_songs)

    # Next in Loop
    def next(self):
        if not self.current_playlist or self.current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        if not self.remaining_songs:
            raise RuntimeError("No songs left to play")

        idx = random.randrange(len(self.remaining_songs))
        selected_song = self.remaining_songs[idx]

        # Remove the selectedSong from the list. (Swap and pop to remove in O(1))
        self.remaining_songs[idx], self.remaining_songs[-1] = (
            self.remaining_songs[-1], self.remaining_songs[idx]
        )
        self.remaining_songs.pop()

        self.history.append(selected_song)
        return selected_song

    def has_previous(self):
        return len(self.history) > 0

    def previous(self):
        if not self.history:
            raise RuntimeError("No previous song available.")

        song = self.history.pop()
        return song
