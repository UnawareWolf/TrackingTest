import typing as ty


class CVObject():

    def __init__(
        self,
        box: ty.List[int],
        detection_score: float,
        detected_class: str,
        obj_id: int
    ):
        self.detection_score = detection_score
        self.detected_class = detected_class
        if detected_class == 'person':
            self.colour = (0, 255, 0)
        else:
            self.colour = (0, 0, 255)
        
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
        self.vel_x = self.loc[0] - prev_obj.loc[0]


    def update_loc(self):
        self.loc = (self.loc[0] + self.vel_x, self.loc[1])
    

    def get_top_left(self) -> tuple[int, int]:
        return (int(self.loc[0] - self.width / 2), int(self.loc[1] - self.height / 2))
    

    def get_bottom_right(self) -> tuple[int, int]:
        return (int(self.loc[0] + self.width / 2), int(self.loc[1] + self.height / 2))


    def get_text_loc(self) -> tuple[int, int]:
        return (int(self.loc[0] - 10 - self.width / 2), int(self.loc[1] - 20 - self.height / 2))


    def is_on_screen(self, vid_width: int, vid_height: int) -> bool:
        return (self.loc[0] >= 0 and self.loc[0] <= vid_width
                and self.loc[1] >= 0 and self.loc[1] <= vid_height)
