from FrameMap import FrameMap
from CVObject import CVObject

import typing as ty


ALLOWED_SIZE_RATIO = 2
OBJECT_DELETION_TIMER = 100
DISTANCE_THRESHOLD = 150


def track_objects(
    previous_detections: ty.List[CVObject],
    current_detections: ty.List[CVObject],
    vid_width: int,
    vid_height: int
):

    frame_map = map_frames(previous_detections, current_detections)
    frame_map.update_ids()
    frame_map.update_velocities()
    track_unmapped_objects(frame_map, previous_detections, current_detections, vid_width, vid_height)


def get_distance(prev_obj: CVObject, current_obj: CVObject) -> float:
    distance_x = prev_obj.loc[0] - current_obj.loc[0]

    return abs(prev_obj.vel_x - distance_x)


def within_size_ratio(prev_obj: CVObject, current_obj: CVObject) -> bool:
    height_ratio = prev_obj.height / current_obj.height
    width_ratio = prev_obj.width / current_obj.width

    return (height_ratio > 1 / ALLOWED_SIZE_RATIO and height_ratio < ALLOWED_SIZE_RATIO and
            width_ratio > 1 / ALLOWED_SIZE_RATIO and width_ratio < ALLOWED_SIZE_RATIO)


def map_frames(previous_detections: ty.List[CVObject], current_detections: ty.List[CVObject]) -> FrameMap:
    frame_map = FrameMap(DISTANCE_THRESHOLD)
    for current_obj in current_detections:
        for prev_obj in previous_detections:
            distance = get_distance(prev_obj, current_obj)
            if distance < DISTANCE_THRESHOLD and within_size_ratio(prev_obj, current_obj):
                frame_map.update_mapping(prev_obj, current_obj, distance)

    return frame_map


def track_unmapped_objects(
    frame_map: FrameMap,
    previous_detections: ty.List[CVObject],
    current_detections: ty.List[CVObject],
    vid_width: int,
    vid_height: int
):

    for prev_obj in previous_detections:
        if (not frame_map.contains_prev(prev_obj)
                and prev_obj.detected_class == 'person'
                and prev_obj.deletion_timer < OBJECT_DELETION_TIMER):
            if not prev_obj.draw:
                prev_obj.deletion_timer += 1
            prev_obj.draw = False
            prev_obj.update_loc()
            if prev_obj.is_on_screen(vid_width, vid_height):
                current_detections.append(prev_obj)
