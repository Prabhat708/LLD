from strategies.PlayStrategy import PlayStrategy


class SequentialPlayStrategy(PlayStrategy):
    def __init__(self):
        self.current_playlist = None
        self.current_index = -1

    def set_playlist(self, playlist):
        self.current_playlist = playlist
        self.current_index = -1

    def has_next(self):
        return (self.current_index + 1) < self.current_playlist.get_size()

    # Next in Loop
    def next(self):
        if not self.current_playlist or self.current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        self.current_index += 1
        return self.current_playlist.get_songs()[self.current_index]

    def has_previous(self):
        return (self.current_index - 1) > 0

    # previous in Loop
    def previous(self):
        if not self.current_playlist or self.current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        self.current_index -= 1
        return self.current_playlist.get_songs()[self.current_index]
