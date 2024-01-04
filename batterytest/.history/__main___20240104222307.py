import pyaudio
import numpy as np
import time

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 500  # Minimum audio amplitude to consider as sound

if __name__ == "__main__":
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Listening for audio...")

    while True:
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        if np.any(data > THRESHOLD):
            print("Audio detected. Starting loop...")
            start_time = time.time()
            break

    while True:
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        if np.all(data < THRESHOLD):
            end_time = time.time()
            print(f"No audio detected. Loop ended. Duration: {end_time - start_time} seconds")
            break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
