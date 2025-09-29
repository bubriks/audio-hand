# Hand audio

Simple music player that utilizes [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html).

## Usage

This solution can be run by creating a new AudioHands object.

## How it works

The decision of the action is based on the location of various points within the hand, described in the x, y, and z axes.

![MediaPipe hand landmarks](https://raw.githubusercontent.com/bubriks/audio-hand/main/hand.png) 

## What it can do

- Change volume
![Volume](https://raw.githubusercontent.com/bubriks/audio-hand/main/volume.png) 
- Show song details
![Info](https://raw.githubusercontent.com/bubriks/audio-hand/main/info.png) 
- Start/stop playing
![Start/stop](https://raw.githubusercontent.com/bubriks/audio-hand/main/stop.png) 
- Switch song
![Switch](https://raw.githubusercontent.com/bubriks/audio-hand/main/switch.png) 

## how to use it

### Requirements

Needs VLC player, on linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install vlc libvlc-dev
```

### Instalation

```bash
git clone https://github.com/bubriks/audio-hand
cd audio-hand/
python3 -m venv .venv
source .venv/bin/activate
pip install numpy opencv-python mediapipe python-vlc
```

### Run

When inside the repository folder execute the following command to start.

```bash
python3 hand_controls.py
```
