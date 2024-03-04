import sounddevice as sd

def print_device_info():
    device_list = sd.query_devices()
    
    for i, device in enumerate(device_list):
        print(f"Device {i} - {device['name']}")
        print(f"  Default Sample Rate: {device['default_samplerate']} Hz")
        print(f"  Channels: {device['max_input_channels']}")
        print(f"  Input Device: {device['max_input_channels'] > 0}")
        print(f"  Output Device: {device['max_output_channels'] > 0}")
        print()

if __name__ == "__main__":
    print_device_info()

