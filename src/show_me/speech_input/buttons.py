#!/usr/bin/env python3

import signal
import pyaudio
import RPi.GPIO as GPIO
import wave
from show_me.speech_input.transcribe import transcribe 
from show_me.inky_display.image_display import display_prompt

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ["A", "B", "C", "D"]

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

heldDown = [False, False, False, False]
heldDownTime = [0, 0, 0, 0]

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second

filename = "output.wav"


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button_down(pin):
    frames = []

    def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        # If len(data) is less than requested frame_count, PyAudio automatically
        # assumes the stream is finished, and the stream stops.

        if GPIO.input(pin) != 0:
            return (None, pyaudio.paComplete)

        return (None, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
        input_device_index=1,
        stream_callback=callback,
    )

    while stream.is_active():
        continue

    print("Stopping recording.")
    stream.close()

    # Release PortAudio system resources (6)
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()

    prompt = transcribe(filename)
    display_prompt(prompt)


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button_down, bouncetime=250)

signal.pause()
