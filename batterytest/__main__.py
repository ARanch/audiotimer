import pyaudio
import numpy as np
import time
from pynput import keyboard

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 10000  # Audio level threshold for detecting sound
MAX_LEVEL = 32768  # Max level for 16-bit audio
BUFFER_TIME = 3  # Buffer time in seconds for countdown
BAR_LENGTH = 50  # Length of the volume bar

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream for audio input
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Listening for audio... Press 'q' to quit early.")

def on_press(key):
    try:
        # Stop the listener if 'q' is pressed
        if key.char == 'q':
            return False
    except AttributeError:
        pass

def create_volume_bar(level, max_level, bar_length, threshold):
    """Create a graphical representation of the volume level."""
    threshold_index = int(bar_length * threshold / max_level)
    volume_index = int(bar_length * level / max_level)
    bar = [' '] * bar_length
    for i in range(bar_length):
        if i < volume_index:
            bar[i] = '='
        if i == threshold_index:
            bar[i] = '|'
    return ''.join(bar)

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

        # Create and display the volume bar
        volume_bar = create_volume_bar(current_level, MAX_LEVEL, BAR_LENGTH, THRESHOLD)
        print(f"Volume: [{volume_bar}] {current_level}/{MAX_LEVEL}", end='\r')

        # Check if the current audio level exceeds the threshold
        if current_level > THRESHOLD:
            if not start_time:
                print("\nAudio detected. Starting timer...")
                start_time = time.time()
            audio_detected = True
            buffer_start = None  # Reset buffer timer
        # Check if sound has stopped
        elif audio_detected:
            if buffer_start is None:
                buffer_start = time.time()  # Start buffer timer
            else:
                remaining_time = BUFFER_TIME - (time.time() - buffer_start)
                if remaining_time <= 0:
                    end_time = time.time()
                    break
                print(f"Countdown before stopping: {int(remaining_time)}s", end='\r')

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
