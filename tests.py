from CVObject import CVObject
from FrameMap import FrameMap
from tracking import *

import unittest


class TrackingTest(unittest.TestCase):

# Tests for CVObject

    def test_calculate_velocity(self):
        prev_obj = CVObject([20, 20, 30, 80], 0.8, 'person', 0)
        cv_obj = CVObject([50, 20, 30, 80], 0.8, 'person', 1)
        cv_obj.calculate_velocity(prev_obj)
        self.assertEqual(cv_obj.vel_x, 30)
    
    def test_update_loc(self):
        cv_obj = CVObject([50, 20, 30, 80], 0.8, 'person', 1)
        cv_obj.vel_x = 10
        cv_obj.update_loc()
        self.assertEqual(cv_obj.loc, (75, 60))
    
    def test_get_top_left(self):
        cv_obj = CVObject([50, 20, 30, 80], 0.8, 'person', 1)
        self.assertEqual(cv_obj.get_top_left(), (50, 20))
    
    def test_get_bottom_right(self):
        cv_obj = CVObject([50, 20, 30, 80], 0.8, 'person', 1)
        self.assertEqual(cv_obj.get_bottom_right(), (80, 100))
    
    def test_is_on_screen(self):
        cv_obj = CVObject([50, 20, 30, 80], 0.8, 'person', 1)
        self.assertTrue(cv_obj.is_on_screen(70, 70))
    
    def test_is_not_on_screen(self):
        cv_obj = CVObject([50, 20, 30, 80], 0.8, 'person', 1)
        self.assertFalse(cv_obj.is_on_screen(60, 70))

# Tests for FrameMap

    def test_update_mapping(self):
        cv_obj_1 = CVObject([50, 20, 30, 80], 0.8, 'person', 0)
        cv_obj_2 = CVObject([60, 30, 30, 80], 0.8, 'person', 1)
        cv_obj_3 = CVObject([57, 26, 30, 80], 0.8, 'person', 2)

        frame_map = FrameMap(20)
        dist_1 = get_projected_distance(cv_obj_1, cv_obj_2)
        frame_map.update_mapping(cv_obj_1, cv_obj_2, dist_1)

        # mapping should update as cv_obj_3 is closer
        dist_2 = get_projected_distance(cv_obj_3, cv_obj_2)
        frame_map.update_mapping(cv_obj_3, cv_obj_2, dist_2)

        self.assertIn(cv_obj_3, frame_map._prev_object_map)
        self.assertIn(cv_obj_2, frame_map._current_object_map)
        self.assertNotIn(cv_obj_1, frame_map._prev_object_map)
        self.assertEqual(frame_map._current_distance_map[cv_obj_2], dist_2)
    
    def test_update_ids(self):
        cv_obj_1 = CVObject([50, 20, 30, 80], 0.8, 'person', 0)
        cv_obj_2 = CVObject([60, 30, 30, 80], 0.8, 'person', 1)
        frame_map = FrameMap(20)
        frame_map._current_object_map[cv_obj_2] = cv_obj_1
        frame_map._prev_object_map[cv_obj_1] = cv_obj_2
        frame_map.update_ids()
        self.assertEqual(cv_obj_2.obj_id, 0)

# Tests for tracking

    def test_within_size_ratio(self):
        cv_obj_1 = CVObject([50, 20, 30, 80], 0.8, 'person', 0)
        cv_obj_2 = CVObject([60, 30, 59, 41], 0.8, 'person', 1)
        self.assertTrue(within_size_ratio(cv_obj_1, cv_obj_2))
    
    def test_not_within_size_ratio(self):
        cv_obj_1 = CVObject([50, 20, 30, 80], 0.8, 'person', 0)
        cv_obj_2 = CVObject([60, 30, 60, 41], 0.8, 'person', 1)
        cv_obj_3 = CVObject([60, 30, 30, 160], 0.8, 'person', 1)
        self.assertFalse(within_size_ratio(cv_obj_1, cv_obj_2))
        self.assertFalse(within_size_ratio(cv_obj_1, cv_obj_3))
    
    def test_get_projected_distance(self):
        cv_obj_1 = CVObject([56, 34, 30, 80], 0.8, 'person', 0)
        cv_obj_2 = CVObject([58, 30, 30, 80], 0.8, 'person', 1)
        cv_obj_1.vel_x = -1

        dist_1 = get_projected_distance(cv_obj_1, cv_obj_2)
        self.assertEqual(dist_1, 5)
    
    def test_map_frames(self):
        cv_obj_1 = CVObject([50, 20, 30, 80], 0.8, 'person', 0)
        cv_obj_2 = CVObject([60, 30, 30, 80], 0.8, 'person', 1)
        cv_obj_3 = CVObject([57, 26, 30, 80], 0.8, 'person', 2)
        frame_map = map_frames([cv_obj_2], [cv_obj_1, cv_obj_3])
        self.assertIn(cv_obj_2, frame_map._prev_object_map)
        self.assertIn(cv_obj_3, frame_map._current_object_map)


if __name__ == "__main__":
    unittest.main()