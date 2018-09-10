import unittest, math
import numpy as np

import utils


class CalcDistanceTest(unittest.TestCase):
	def test_works_as_expected(self):
		'''utils.calc_distance correctly calculates the distance between two points'''
		pairs = [
			[[0,0], [1,1]],
			[[0,0], [0,1]],
			[[5,2], [2,5]],
			[[-1,3], [10,0]]
		]

		for pair in pairs:
			distance = utils.calc_distance(*pair)
			expected_distance = math.sqrt((pair[1][0] - pair[0][0])**2 + (pair[1][1] - pair[0][1])**2)
			self.assertEqual(distance, expected_distance)

class CalcAngleTest(unittest.TestCase):
	def test_works_as_expected(self):
		'''utils.calc_angle correctly calculates the angle between two points'''
		pairs = [
			[[0,0], [1,0]],
			[[1,0], [0,0]],
			[[0,0], [1,1]],
			[[0,0], [0,1]],
			[[1,1], [0,0]],
			[[0,0], [1,2]],
			[[0,1], [1,0]]
		]
		expected_angles = [
			0,
			np.pi,
			np.pi/4,
			np.pi/2,
			5*np.pi/4,
			math.atan(2),
			7*np.pi/4
		]

		for pair, expected_angle in zip(pairs, expected_angles):
			angle = utils.calc_angle(*pair)
			self.assertEqual(round(angle,10), round(expected_angle, 10))


if __name__ == '__main__':
	unittest.main()