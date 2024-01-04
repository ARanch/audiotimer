import pyaudio
import numpy as np
import time
from pynput import keyboard

# Constants
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels (1 for mono)
RATE = 44100  # Sampling rate (44.1kHz)
CHUNK = 1024  # Size of each read from the buffer
THRESHOLD = 400  # Audio level threshold for detecting sound
BUFFER_TIME = 3  # Buffer time in seconds

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream for audio input
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Listening for audio... Press 'q' to quit early.")

# Define a callback function for keypress events
def on_press(key):
    try:
        # Stop the listener if 'q' is pressed
        if key.char == 'q':
            return False
    except AttributeError:
        pass

# Start a keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

start_time = None
audio_detected = False
buffer_start = None

try:
    while True:
        # Check if the stream is active
        if not stream.is_active():
            raise RuntimeError("Audio stream is not active. Please check your microphone.")

        # Read data from the audio stream
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        current_level = np.max(data)

        # Check if the current audio level exceeds the threshold
        if current_level > THRESHOLD:
            if not start_time:
                print("\nAudio detected. Starting timer...")
                start_time = time.time()
            audio_detected = True
            buffer_start = None  # Reset buffer timer
        # Check if sound has stopped
        elif audio_detected and (buffer_start is None or time.time() - buffer_start >= BUFFER_TIME):
            if buffer_start is None:
                buffer_start = time.time()  # Start buffer timer
            elif time.time() - buffer_start >= BUFFER_TIME:
                end_time = time.time()
                break

        # Print the current audio level
        print(f"Current audio level: {current_level}", end='\r')
        time.sleep(0.1)  # Delay for 0.1 seconds

        # Check for keypress to quit early
        if not listener.running and start_time:
            end_time = time.time()
            break
except KeyboardInterrupt:
    end_time = time.time()
except RuntimeError as e:
    print(e)
finally:
    # Close the audio stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

# Calculate and print the duration if audio was detected
if start_time:
    duration = end_time - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = f"{int(hours)}h:{int(minutes):02d}m:{int(seconds):02d}s"
    print(f"\nDuration: {formatted_duration}")

    # Write the duration to a file
    with open("duration.txt", "w") as file:
        file.write(f"Duration: {formatted_duration}")
else:
    print("No audio detected.")
