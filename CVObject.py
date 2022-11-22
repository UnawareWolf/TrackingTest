import typing as ty


GREEN = (0, 255, 0)
RED = (0, 0, 255)


class CVObject():

    def __init__(
        self,
        box: ty.List[int],
        detection_score: float,
        detected_class: str,
        obj_id: int
    ):
        """Object representing a single bounding box in a single frame. This
        can be used to track objects across frames.

        Args:
            box: bounding box data in a list containing first their top left corner
                coordinates (x and y pixel coordinates) then their width and height.
            detection_score: confidence between 0 (low) and 1 (high) that the object
                is of the detected class.
            detected_class: the class of the detected object in the bounding box.
            obj_id: a unique id for this video that will be overwritten if this
                object is deemed to match a previous object.
        """
        self.detection_score = detection_score
        self.detected_class = detected_class
        if detected_class == 'person':
            self.colour = GREEN
        else:
            self.colour = RED
        
        self.width = box[2]
        self.height = box[3]

        pt1 = (box[0], box[1])
        pt2 = (box[0] + box[2], box[1] + box[3])
        self.loc = ((pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2)

        self.obj_id = obj_id
        self.vel_x = 0
        self.draw = True
        self.deletion_timer = 0


    def calculate_velocity(self, prev_obj: 'CVObject') -> float:
        """Calculate the velocity, in pixels per frame, of the CVObject base
        on its location relative to a CVObject in the previous frame with the
        same id. Only the horizontal velocities are used because the vertical
        velocities were mainly due to the recording vehicle going over bumps,
        decreasing the accuracy.
        """
        self.vel_x = self.loc[0] - prev_obj.loc[0]


    def update_loc(self):
        """Update the projected location in the next frame based on the current
        velocity.
        """
        self.loc = (self.loc[0] + self.vel_x, self.loc[1])
    

    def get_top_left(self) -> tuple[int, int]:
        """Return tuple of the top left coordinate of the bounding box to be drawn.
        """
        return (int(self.loc[0] - self.width / 2), int(self.loc[1] - self.height / 2))
    

    def get_bottom_right(self) -> tuple[int, int]:
        """Return tuple of the bottom right coordinate of the bounding box to be drawn.
        """
        return (int(self.loc[0] + self.width / 2), int(self.loc[1] + self.height / 2))


    def get_text_loc(self) -> tuple[int, int]:
        """Return tuple containing the coordinate to write the obj_id.
        """
        return (int(self.loc[0] - 10 - self.width / 2), int(self.loc[1] - 20 - self.height / 2))


    def is_on_screen(self, vid_width: int, vid_height: int) -> bool:
        """Return true if the centre point of loc is within the screen dimensions.
        """
        return (self.loc[0] >= 0 and self.loc[0] <= vid_width
                and self.loc[1] >= 0 and self.loc[1] <= vid_height)
