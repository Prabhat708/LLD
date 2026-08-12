from device.IAudioOutputDevice import IAudioOutputDevice
from external.BluetoothSpeakerAPI import BluetoothSpeakerAPI


class BluetoothSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, api):
        self.bluetooth_api = api

    def play_audio(self, song):
        payload = song.get_title() + " by " + song.get_artist()
        self.bluetooth_api.play_sound_via_bluetooth(payload)
