# test_google_cloud_speech.py
from google.cloud import speech

client = speech.SpeechClient()

def transcribe_audio():
    audio = speech.RecognitionAudio(uri="gs://cloud-samples-data/speech/brooklyn_bridge.raw")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    transcribe_audio()

