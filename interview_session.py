import os
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr

DEVICE_INDEX = 1 
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 10  # Fallback duration in seconds

def record_audio(filename="response.wav"):
    print("➡️ Press Enter to start recording your answer...")
    input()
    print("🎙️ Recording... Press Enter again to stop (or wait 10 sec).")

    sd.default.device = (DEVICE_INDEX, None)
    sd.default.samplerate = SAMPLE_RATE
    sd.default.channels = CHANNELS

    try:
        recording = []

        def callback(indata, frames, time, status):
            recording.append(indata.copy())

        stream = sd.InputStream(callback=callback)
        with stream:
            if not input_with_timeout(DURATION):
                print("⏱️ Timeout reached. Auto-stopping...")
            stream.stop()

        audio_data = np.concatenate(recording, axis=0)
        write(filename, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))
        print("✅ Recording saved.")
        return filename
    except Exception as e:
        print(f"❌ Recording error: {e}")
        return None

def input_with_timeout(timeout):
    import threading

    user_input = []

    def wait_input():
        input()
        user_input.append(True)

    thread = threading.Thread(target=wait_input)
    thread.start()
    thread.join(timeout)
    return bool(user_input)

def transcribe_audio(filename):
    print("📝 Transcribing your response...")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "[❌ Could not understand audio]"
    except sr.RequestError as e:
        return f"[❌ Google API error: {e}]"

def run_session():
    print("\n🎤 Welcome to the AI Interview Session!\n")

    if not os.path.exists("interview_questions.txt"):
        print("⚠️ 'interview_questions.txt' not found.")
        return

    with open("interview_questions.txt", "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip() and line.strip()[0].isdigit()]

    if not questions:
        print("⚠️ No valid questions found.")
        return

    # Prepare transcript file
    with open("transcript.txt", "w", encoding="utf-8") as out:

        for idx, question in enumerate(questions, 1):
            print(f"\n❓ Question {idx}:\n{question}")
            out.write(f"Q{idx}: {question}\n")
            audio_file = record_audio()
            if audio_file:
                answer = transcribe_audio(audio_file)
                print(f"\n🗣️ Your Answer:\n{answer}")
                out.write(f"A{idx}: {answer}\n\n")
            else:
                print("⚠️ Skipped due to recording issue.")
                out.write(f"A{idx}: [Recording failed]\n\n")
            time.sleep(1)

    print("\n✅ Interview completed. Transcript saved to 'transcript.txt'.")
if __name__ == "__main__":
    run_session()


