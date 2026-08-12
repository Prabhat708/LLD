class AudioEngine:
    def __init__(self):
        self.current_song = None
        self.song_is_paused = False

    def get_current_song_title(self):
        if self.current_song:
            return self.current_song.get_title()
        return ""

    def is_paused(self):
        return self.song_is_paused

    def play(self, audio_output_device, song):
        if song is None:
            raise RuntimeError("Cannot play a null song.")

        # Resume if same song was paused
        if self.song_is_paused and song is self.current_song:
            self.song_is_paused = False
            print(f"Resuming song: {song.get_title()}")
            audio_output_device.play_audio(song)
            return

        self.current_song = song
        self.song_is_paused = False
        print(f"Playing song: {song.get_title()}")
        audio_output_device.play_audio(song)

    def pause(self):
        if self.current_song is None:
            raise RuntimeError("No song is currently playing to pause.")
        if self.song_is_paused:
            raise RuntimeError("Song is already paused.")

        self.song_is_paused = True
        print(f"Pausing song: {self.current_song.get_title()}")
