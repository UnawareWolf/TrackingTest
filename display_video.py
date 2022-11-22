from math import floor
from typing import NoReturn
from CVObject import CVObject
from tracking import track_objects

import cv2
import json
import numpy
import typing as ty


THRESHOLD_TO_DRAW = 0.7


def open_video(path: str) -> cv2.VideoCapture:
    """Opens a video file.

    Args:
        path: the location of the video file to be opened

    Returns:
        An opencv video capture file.
    """
    video_capture = cv2.VideoCapture(path)
    if not video_capture.isOpened():
        raise RuntimeError(f'Video at "{path}" cannot be opened.')
    return video_capture


def get_frame_dimensions(video_capture: cv2.VideoCapture) -> tuple[int, int]:
    """Returns the frame dimension of the given video.

    Args:
        video_capture: an opencv video capture file.

    Returns:
        A tuple containing the height and width of the video frames.

    """
    return video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), video_capture.get(
        cv2.CAP_PROP_FRAME_HEIGHT
    )


def get_frame_display_time(video_capture: cv2.VideoCapture) -> int:
    """Returns the number of milliseconds each frame of a VideoCapture should be displayed.

    Args:
        video_capture: an opencv video capture file.

    Returns:
        The number of milliseconds each frame should be displayed for.
    """
    frames_per_second = video_capture.get(cv2.CAP_PROP_FPS)
    return floor(1000 / frames_per_second)


def is_window_open(title: str) -> bool:
    """Checks to see if a window with the specified title is open."""

    # all attempts to get a window property return -1 if the window is closed
    return cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) >= 1


def read_video_detections(video_name: str) -> dict:
    json_name = "{}_detections.json".format(video_name.split(".")[0])
    detections = {}
    with open(json_name) as f:
        detections = json.load(f)
    return detections


def draw_bounding_boxes(image: numpy.ndarray, detection_frame: ty.List[CVObject]) -> numpy.ndarray:
    for cv_obj in detection_frame:
        if cv_obj.detection_score >= THRESHOLD_TO_DRAW and cv_obj.draw:
            image = cv2.rectangle(image, cv_obj.get_top_left(), cv_obj.get_bottom_right(), cv_obj.colour, 4, 0)
            if cv_obj.detected_class == 'person':
                image = cv2.putText(image, str(cv_obj.obj_id), cv_obj.get_text_loc(), cv2.FONT_HERSHEY_SIMPLEX, 2, cv_obj.colour, 2)

    return image


def parse_detections(detections_json: dict) -> ty.List[ty.List[CVObject]]:
    frame_no = 1
    frames = []
    obj_id = 0
    while str(frame_no) in detections_json:
        detection = detections_json[str(frame_no)]
        cv_objects = []
        for i in range(len(detection['bounding boxes'])):
            cv_objects.append(
                CVObject(detection['bounding boxes'][i],
                detection['detection scores'][i],
                detection['detected classes'][i],
                obj_id)
            )
            obj_id += 1
        frames.append(cv_objects)
        frame_no += 1
    return frames


def main(video_path: str, title: str) -> NoReturn:
    """Displays a video at half size until it is complete or the 'q' key is pressed.

    Args:
        video_path: the location of the video to be displayed
        title: the title to display in the video window
    """

    video_capture = open_video(video_path)
    width, height = get_frame_dimensions(video_capture)
    wait_time = get_frame_display_time(video_capture)
    detections_json = read_video_detections(video_path)
    detections = parse_detections(detections_json)

    try:
        # read the first frame
        success, frame = video_capture.read()
        frame_no = 0

        # create the window
        cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)

        # run whilst there are frames and the window is still open
        while success and is_window_open(title):
            if frame_no > 0:
                track_objects(detections[frame_no - 1], detections[frame_no], width, height)

            image = draw_bounding_boxes(frame, detections[frame_no])

            # shrink it
            smaller_image = cv2.resize(image, (floor(width // 2), floor(height // 2)))
            # image = draw_bounding_boxes(smaller_image, detections[frame_no])

            # display it
            cv2.imshow(title, smaller_image)

            # test for quit key
            if cv2.waitKey(wait_time) == ord("q"):
                break

            # read the next frame
            success, frame = video_capture.read()
            frame_no += 1
    finally:
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    VIDEO_PATH = "resources/video_3.mp4"
    main(VIDEO_PATH, "My Video")
