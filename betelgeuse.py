import sys
import signal
import sounddevice as sd
import scipy.io.wavfile as wav
from google.cloud import speech
import time

sys.path.append('path/to/snowboy/swig/Python')  # Update this path
import snowboydecoder

model = "Betelgeuse.pmdl"  # Path to your Snowboy model file
sensitivity = 0.5

sample_rate = 16000

def detected_callback():
    print("Wake word 'Betelgeuse' detected!")
    record_and_process()

def record_and_process():
    print("Recording for 5 seconds...")
    audio = sd.rec(int(5 * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write('wake_word_output.wav', sample_rate, audio)
    print("Recording finished")

    # Process with Google Cloud Speech-to-Text
    client = speech.SpeechClient()
    with open('wake_word_output.wav', 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

def signal_handler(signal, frame):
    detector.terminate()
    sys.exit(0)

if __name__ == "__main__":
    detector = snowboydecoder.HotwordDetector(model, sensitivity=sensitivity)
    print('Listening for wake word "Betelgeuse"... Press Ctrl+C to exit')

    # Capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector.start(detected_callback=detected_callback)

