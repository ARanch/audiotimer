# Audio timer
This small program starts listening for an audio input on the system microphone. When a set audio level threshold is reached, a timer is started. When the audio level is reduced below the threshold, the timer is stopped after a short countdown, and the timespan is logged.

`python -m pip install audiotimer`

install requirements:
`pip install -r requirements.txt`


run using: 
`python audiotimer`