import pyaudio

def list_audio_devices():
    audio = pyaudio.PyAudio()
    print("Available audio devices:")
    
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        print(f"Index: {i}, Name: {device_info['name']}, Input Channels: {device_info['maxInputChannels']}, Output Channels: {device_info['maxOutputChannels']}")
    
    audio.terminate()

if __name__ == "__main__":
    list_audio_devices()