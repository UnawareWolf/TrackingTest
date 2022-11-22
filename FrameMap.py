from collections import defaultdict
from CVObject import CVObject


class FrameMap:

    def __init__(self, threshold: int):
        self._prev_object_map = {}
        self._current_object_map = {}
        self._prev_distance_map = defaultdict(lambda: threshold)
        self._current_distance_map = defaultdict(lambda: threshold)


    def update_mapping(self, prev_obj: CVObject, current_obj: CVObject, distance: int):
        if (distance < self._prev_distance_map[prev_obj] and
                distance < self._current_distance_map[current_obj]):
            self._prev_object_map[prev_obj] = current_obj
            self._current_object_map[current_obj] = prev_obj
            self._prev_distance_map[prev_obj] = distance
            self._current_distance_map[current_obj] = distance

    
    def contains_prev(self, prev_obj: CVObject) -> bool:
        return prev_obj in self._prev_object_map

    
    def update_ids(self):
        for prev_obj, current_obj in self._prev_object_map.items():
            current_obj.obj_id = prev_obj.obj_id

    
    def update_velocities(self):
        for prev_obj, current_obj in self._prev_object_map.items():
            current_obj.calculate_velocity(prev_obj)
