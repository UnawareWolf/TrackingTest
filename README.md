# Tracking Test

This project displays coloured bounding boxes on top of dash cam footage. The bounding boxes contain objects, such as a person or a car, that have been detected in the video using a pre-existing model. Different colours are used for different object classes as follows:

1. person: green
1. car: red
1. bicycle: blue
1. truck: black
1. bus: yellow
1. motorbike: purple
1. default: white

The code attempts to track pedestrians from frame to frame based on the location, size and velocity of bounding boxes. The velocity of the bounding box is calculated using the distance moved by pedestrians that have already been tracked across at least one frame. Any pedestrians that are tracked across multiple frames will have the same identifier displayed over their head. Bounding boxes that have not been tracked from a previous frame will have identifiers that update every frame.

The video can be displayed by running the `display_video.py` script. This calls functions from `tracking.py` which contains the code to track objects across frames. The classes `CVObject` and `FrameMap` have been created to make it easier to create a 1 to 1 mapping of objects across frames. `tests.py` contains unit tests that can be run as a script.