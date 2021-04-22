# Hand audio

Simple music player that utilizes [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html).

## Usage

This solution can be run by creating new AudioHands object.

## How it works

The solution decides the action based on location of various points within hand, described in x,y and z axes.

![MediaPipe hand landmarks](https://google.github.io/mediapipe/images/mobile/hand_landmarks.png) 

## What it can do

- Change valume
- Show song details
- Start/stop playing
- Switch song

## how to use it

### Instalation

This solution requires Python and the following libraries:

- pip install numpy
- pip install opencv-python
- pip install mediapipe
- pip install python-vlc

### Run

When inside the repository folder execute the following command to start.

python hand_controls.py