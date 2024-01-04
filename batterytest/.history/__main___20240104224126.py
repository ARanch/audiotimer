import pyaudio
import numpy as np
import time
from pynput import keyboard

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 500  # Adjust this as needed

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Listening for audio... Press 'q' to quit early.")

def on_press(key):
    try:
        if key.char == 'q':
            return False
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

start_time = None
try:
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        current_level = np.max(data)
        print(f"Current audio level: {current_level}", end='\r')

        if current_level > THRESHOLD and not start_time:
            print("\nAudio detected. Starting timer...")
            start_time = time.time()

        if not listener.running and start_time:
            end_time = time.time()
            break
except KeyboardInterrupt:
    end_time = time.time()

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()

if start_time:
    duration = end_time - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = f"{int(hours)}:{int(minutes)}:{seconds:.2f}"
    print(f"Duration: {formatted_duration}")

    # Write to file
    with open("duration.txt", "w") as file:
        file.write(f"Duration: {formatted_duration}")
else:
    print("No audio detected.")
