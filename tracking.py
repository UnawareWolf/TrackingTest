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
    """Map the ids and velocities of the CVObjects of previous frames onto
    the CVObjects in the current frame.

    Args:
        previous_detections: list of CVObjects from the previous frame.
        current_detections: list of CVObjects from the current frame.
        vid_width: width of the video to display.
        vid_height: height of the video to display.
    """
    frame_map = map_frames(previous_detections, current_detections)
    frame_map.update_ids()
    frame_map.update_velocities()
    track_unmapped_objects(frame_map, previous_detections, current_detections, vid_width, vid_height)


def get_projected_distance(prev_obj: CVObject, current_obj: CVObject) -> float:
    """Return the absolute distance, in pixels, between a CVObject in the
    current frame and the projected location of a CVObject from the previous
    frame (projected based on its previous location and velocity).

    Args:
        prev_obj: CVObject from the previous frame.
        current_obj: CVObject from the current frame.
    
    Returns:
        Distance between the centre of the two CVObjects, in pixels.
    """
    distance_x = prev_obj.loc[0] - current_obj.loc[0]

    return abs(prev_obj.vel_x - distance_x)


def within_size_ratio(obj_1: CVObject, obj_2: CVObject) -> bool:
    """Return true if the ratios of width and height of two CVObjects are
    within ALLOWED_SIZE_RATIO.
    """
    height_ratio = obj_1.height / obj_2.height
    width_ratio = obj_1.width / obj_2.width

    return (height_ratio > 1 / ALLOWED_SIZE_RATIO and height_ratio < ALLOWED_SIZE_RATIO and
            width_ratio > 1 / ALLOWED_SIZE_RATIO and width_ratio < ALLOWED_SIZE_RATIO)


def map_frames(previous_detections: ty.List[CVObject], current_detections: ty.List[CVObject]) -> FrameMap:
    """Map CVObjects from the previous frame onto those of the current frame
    that are closest to the projected position.

    Args:
        previous_detections: list of CVObjects from the previous frame.
        current_detections: list of CVObjects from the current frame.
    
    Returns:
        1 to 1 map of CVObjects from the previous to the current frame.
    """
    frame_map = FrameMap(DISTANCE_THRESHOLD)
    for current_obj in current_detections:
        for prev_obj in previous_detections:
            distance = get_projected_distance(prev_obj, current_obj)
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
    """Add the unmapped CVObjects (those from the previous frame that did not
    map onto the current frame) to the list for the current frame so that they
    have a chance of mapping onto the next frame.
    """
    for prev_obj in previous_detections:
        # Check that the CVObject is of class 'person' and did not map onto the
        # current frame and has been waiting for a mapping for less than 100
        # frames.
        if (not frame_map.contains_prev(prev_obj)
                and prev_obj.detected_class == 'person'
                and prev_obj.deletion_timer < OBJECT_DELETION_TIMER):

            # Update timer so that the CVObject will be removed after 100 frames
            prev_obj.deletion_timer += 1

            # Set draw to false so that the bounding box is not drawn
            prev_obj.draw = False

            # Update projected location based on current velocity
            prev_obj.update_loc()

            # Only add to the current frame if it is still on screen
            if prev_obj.is_on_screen(vid_width, vid_height):
                current_detections.append(prev_obj)
