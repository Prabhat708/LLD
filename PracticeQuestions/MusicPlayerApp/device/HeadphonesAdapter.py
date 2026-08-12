from device.IAudioOutputDevice import IAudioOutputDevice
from external.HeadphonesAPI import HeadphonesAPI


class HeadphonesAdapter(IAudioOutputDevice):
    def __init__(self, api):
        self.headphones_api = api

    def play_audio(self, song):
        payload = song.get_title() + " by " + song.get_artist()
        self.headphones_api.play_sound_via_jack(payload)
