import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5
def record_audio(filename="recorded.wav"):
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wav

    DURATION = 5
    SAMPLE_RATE = 16000
    CHANNELS = 1
    DEVICE_INDEX =1  
    try:
        sd.default.device = (DEVICE_INDEX, None)

        print("🎤 Recording...")
        audio_data = sd.rec(int(DURATION * SAMPLE_RATE),
                            samplerate=SAMPLE_RATE,
                            channels=CHANNELS,
                            dtype='int16')
        sd.wait()
        wav.write(filename, SAMPLE_RATE, audio_data)
        print(f"✅ Saved: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error during recording: {e}")
        return None




def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        print("📝 Transcribing...")
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
    except sr.UnknownValueError:
        print("❌ Speech was unintelligible.")
    except sr.RequestError as e:
        print(f"❌ Could not reach speech recognition service: {e}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

def main():
    audio_file = record_audio()
    if audio_file:
        transcribe_audio(audio_file)

if __name__ == "__main__":
    main()

