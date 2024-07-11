# listen_for_wake_word.py
import speech_recognition as sr

recognizer = sr.Recognizer()
wake_word = "Jarvis"

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

if __name__ == "__main__":
    if listen_for_wake_word():
        print("Wake word was detected, proceed with further processing")
    else:
        print("Wake word was not detected, listening again...")

