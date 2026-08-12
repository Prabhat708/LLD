from device.IAudioOutputDevice import IAudioOutputDevice
from external.WiredSpeakerAPI import WiredSpeakerAPI


class WiredSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, api):
        self.wired_api = api

    def play_audio(self, song):
        payload = song.get_title() + " by " + song.get_artist()
        self.wired_api.play_sound_via_cable(payload)
