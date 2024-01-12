# Audio timer
Github: https://github.com/ARanch/audiotimer

This small program starts listening for an audio input on the system microphone. When a set audio level threshold is reached, a timer is started. When the audio level is reduced below the threshold, the timer is stopped after a short countdown, and the timespan is logged.

`python -m pip install audiotimer`

install requirements:
`pip install -r requirements.txt`


run using: 
`python audiotimer`

see -h flag for run-time options.

## Use case
The program is intended to be used as a way of testing the battery life of battery powered loudspeakers. Set the speaker to play a pink noise at a certain level, and leave a laptop with the speaker to listen for when it dies out. 
