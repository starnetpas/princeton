import time
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from google.cloud import speech

recognizer = sr.Recognizer()
wake_word = "Jarvis"
sample_rate = 16000

def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            print(f"You said: {transcription}")
            if wake_word.lower() in transcription.lower():
                print("Wake word detected!")
                return True
            else:
                print("Wake word not detected")
                return False
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return False

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

if __name__ == "__main__":
    while True:
        try:
            if listen_for_wake_word():
                record_and_process()
            # Adding a short pause before listening again
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

