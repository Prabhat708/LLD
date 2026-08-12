from enums.DeviceType import DeviceType
from device.BluetoothSpeakerAdapter import BluetoothSpeakerAdapter
from device.WiredSpeakerAdapter import WiredSpeakerAdapter
from device.HeadphonesAdapter import HeadphonesAdapter
from external.BluetoothSpeakerAPI import BluetoothSpeakerAPI
from external.WiredSpeakerAPI import WiredSpeakerAPI
from external.HeadphonesAPI import HeadphonesAPI


class DeviceFactory:
    @staticmethod
    def create_device(device_type):
        if device_type == DeviceType.BLUETOOTH:
            return BluetoothSpeakerAdapter(BluetoothSpeakerAPI())
        elif device_type == DeviceType.WIRED:
            return WiredSpeakerAdapter(WiredSpeakerAPI())
        else:  # HEADPHONES
            return HeadphonesAdapter(HeadphonesAPI())
