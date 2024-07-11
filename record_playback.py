# record_playback.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Record audio
duration = 5  # seconds
sample_rate = 16000

print("Recording...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished
print("Recording finished")

# Save to a WAV file
wav.write('output.wav', sample_rate, audio)

# Play back the recorded audio
print("Playing back...")
sd.play(audio, samplerate=sample_rate)
sd.wait()  # Wait until playback is finished
print("Playback finished")

