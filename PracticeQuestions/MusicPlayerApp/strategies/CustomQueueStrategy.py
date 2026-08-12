from collections import deque

from strategies.PlayStrategy import PlayStrategy


class CustomQueueStrategy(PlayStrategy):
    def __init__(self):
        self.current_playlist = None
        self.current_index = -1
        self.next_queue = deque()
        self.prev_stack = []

    def _next_sequential(self):
        if self.current_playlist.get_size() == 0:
            raise RuntimeError("Playlist is empty.")
        self.current_index += 1
        return self.current_playlist.get_songs()[self.current_index]

    def _previous_sequential(self):
        if self.current_playlist.get_size() == 0:
            raise RuntimeError("Playlist is empty.")
        self.current_index -= 1
        return self.current_playlist.get_songs()[self.current_index]

    def set_playlist(self, playlist):
        self.current_playlist = playlist
        self.current_index = -1
        self.next_queue.clear()
        self.prev_stack.clear()

    def has_next(self):
        return (self.current_index + 1) < self.current_playlist.get_size()

    def next(self):
        if not self.current_playlist or self.current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        if self.next_queue:
            song = self.next_queue.popleft()
            self.prev_stack.append(song)

            # update index to match queued song
            songs = self.current_playlist.get_songs()
            for i, item in enumerate(songs):
                if item is song:
                    self.current_index = i
                    break
            return song

        # Otherwise sequential
        return self._next_sequential()

    def has_previous(self):
        return (self.current_index - 1) > 0

    def previous(self):
        if not self.current_playlist or self.current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        if self.prev_stack:
            song = self.prev_stack.pop()

            # update index to match stacked song
            songs = self.current_playlist.get_songs()
            for i, item in enumerate(songs):
                if item is song:
                    self.current_index = i
                    break
            return song

        # Otherwise sequential
        return self._previous_sequential()

    def add_to_next(self, song):
        if song is None:
            raise RuntimeError("Cannot enqueue null song.")
        self.next_queue.append(song)
