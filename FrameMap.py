from collections import defaultdict
from CVObject import CVObject


class FrameMap:

    def __init__(self, threshold: int):
        """Map object facilitating the 1 to 1 map of CVObjects from the previous
        to the current frame. 2 maps are used which map the values of one to the
        keys of the other, ensuring that there are no duplicate values.

        Args:
            threshold: the minimum distance between two objects to map them
                across frames.
        """
        self._prev_object_map = {}
        self._current_object_map = {}

        self._prev_distance_map = defaultdict(lambda: threshold)
        self._current_distance_map = defaultdict(lambda: threshold)


    def update_mapping(self, prev_obj: CVObject, current_obj: CVObject, distance: int):
        """Update to map prev_obj to current_obj if the distance is less than that of
        the existing mapping for either CVObject. Both object maps are updated to ensure
        there are no duplicate values.
        """
        if (distance < self._prev_distance_map[prev_obj] and
                distance < self._current_distance_map[current_obj]):
            self._prev_object_map[prev_obj] = current_obj
            self._current_object_map[current_obj] = prev_obj
            self._prev_distance_map[prev_obj] = distance
            self._current_distance_map[current_obj] = distance

    
    def contains_prev(self, prev_obj: CVObject) -> bool:
        """Return true if prev_obj is a key in the previous object map.
        """
        return prev_obj in self._prev_object_map

    
    def update_ids(self):
        """Set the obj_id from the CVObject of the previous frame onto
        the mapped CVObject in the current frame.
        """
        for prev_obj, current_obj in self._prev_object_map.items():
            current_obj.obj_id = prev_obj.obj_id

    
    def update_velocities(self):
        """Update the velocity of the current CVObjects based on how far
        away they are from the corresponding CVObject in the previous frame.
        """
        for prev_obj, current_obj in self._prev_object_map.items():
            current_obj.calculate_velocity(prev_obj)
