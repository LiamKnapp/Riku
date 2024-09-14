import pyaudio, wave, keyboard, numpy, collections, faster_whisper, torch.cuda, os

model = faster_whisper.WhisperModel(model_size_or_path="tiny.en", device='cuda' if torch.cuda.is_available() else 'cpu')
voice_recording_path = "./voice_record.wav"

def transcribe_audio(frames, audio):
    # Transcribe recording using whisper
    with wave.open(voice_recording_path, 'wb') as wf:
        wf.setparams((1, audio.get_sample_size(pyaudio.paInt16), 16000, 0, 'NONE', 'NONE'))
        wf.writeframes(b''.join(frames))
    user_text = " ".join(seg.text for seg in model.transcribe(voice_recording_path, language="en")[0])
    print(f'>>> {user_text}\n', end="", flush=True)
    return user_text

def get_levels(data, long_term_noise_level, current_noise_level):
    pegel = numpy.abs(numpy.frombuffer(data, dtype=numpy.int16)).mean()
    long_term_noise_level = long_term_noise_level * 0.995 + pegel * (1.0 - 0.995)
    current_noise_level = current_noise_level * 0.920 + pegel * (1.0 - 0.920)
    return pegel, long_term_noise_level, current_noise_level

def Get_Speech():
    pegel, long_term_noise_level, current_noise_level = 0.0, 0.0, 0.0  # Initialize pegel here
    ambient_noise_level = 0  # Initialize ambient noise level
    user_input = ""
    while True:
        audio = pyaudio.PyAudio()
        stream = audio.open(rate=16000, format=pyaudio.paInt16, channels=1, input=True, frames_per_buffer=512, input_device_index=1)
        audio_buffer = collections.deque(maxlen=int((16000 // 512) * 0.5))
        frames, voice_activity_detected = [], False

        print("\n\nStart speaking. Or press ',' to type a query. Generate me an image\n", end="", flush=True)
        print("Say, 'Generate me an image' Followed by what you want the image to be to get art work\n", end="", flush=True)
        while True:

            if keyboard.is_pressed(","): # check if the user wants to type the query
                user_input = input("Enter your query: ")  # Get user input and store it in a variable
                break

            data = stream.read(512)
            pegal, long_term_noise_level, current_noise_level = get_levels(data, long_term_noise_level, current_noise_level)
            audio_buffer.append(data)

            if voice_activity_detected:
                frames.append(data)            
                if current_noise_level < ambient_noise_level + 100:
                    break  # voice activity ends 
        
            if not voice_activity_detected and current_noise_level > long_term_noise_level + 300:
                voice_activity_detected = True
                ambient_noise_level = long_term_noise_level
                frames.extend(list(audio_buffer))
        stream.stop_stream()
        stream.close()
        audio.terminate()
        if user_input == "": # if the user did not type a query use the audio
            user_text = transcribe_audio(frames, audio)
            try:
                os.remove(voice_recording_path)
                #print("Voice recording removed")
            except Exception as e:
                print(f"An error occurred: {e}")
            return user_text
        else: # use the users typed query
            return user_input