# Tracking Test

This project displays bounding boxes on top of dash cam footage. The bounding boxes contain objects, such as a person or a car, that have been detected in the video using a pre-existing model.

The code attempts to track pedestrians from frame to frame based on the location, size and velocity of bounding boxes. The velocity of the bounding box is calculated using the distance moved by the pedestrians that have already been tracked across at least one frame. Any pedestrians that are tracked across multiple frames will have the same identifier displayed over their head. Bounding boxes that have not been tracked from a previous frame will have identifiers that update every frame.