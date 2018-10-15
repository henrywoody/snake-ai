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
		input_output_pairs = [
			[[[0,0], [1,0]], 0],
			[[[1,0], [0,0]], np.pi],
			[[[0,0], [1,1]], np.pi/4],
			[[[0,0], [0,1]], np.pi/2],
			[[[1,1], [0,0]], 5*np.pi/4],
			[[[0,0], [1,2]], math.atan(2)],
			[[[0,1], [1,0]], 7*np.pi/4]
		]

		for coord_pair, expected_angle in input_output_pairs:
			angle = utils.calc_angle(*coord_pair)
			self.assertEqual(round(angle,10), round(expected_angle, 10))


class MockObject:
	def __init__(self, position, size):
		self.position = position
		self.size = size

class AreTouchingTest(unittest.TestCase):
	def test_returns_True_if_touching(self):
		'''are_touching returns True if the distance between the two objects is less than or eq to the sum of their sizes'''
		obj_pairs = [
			[MockObject([0,0], 1), MockObject([1,0], 1)],
			[MockObject([0,0], 1), MockObject([1,1], 1)],
			[MockObject([0,0], 5), MockObject([2,2], 2)],
			[MockObject([5,5], 1), MockObject([1,0], 10)],
			[MockObject([0,0], 1), MockObject([-1,0], 1)],
			[MockObject([0,0], 1), MockObject([-1,-1], 2)],
			[MockObject([0,0], 3), MockObject([3,2], 2)]
		]

		for obj_pair in obj_pairs:
			output = utils.are_touching(*obj_pair)
			self.assertTrue(output)

	def test_returns_False_if_not_touching(self):
		'''are_touching returns False if the distance between the two objects is greater than or eq to the sum of their sizes'''
		obj_pairs = [
			[MockObject([0,0], 2), MockObject([5,0], 2)],
			[MockObject([0,5], 2), MockObject([5,0], 3)],
			[MockObject([0,0], 1), MockObject([3,3], 2)],
			[MockObject([5,5], 2), MockObject([0,0], 2)],
			[MockObject([0,0], 2), MockObject([-4.5,0], 2)],
			[MockObject([0,0], 1), MockObject([-5,-5], 5)]
		]

		for obj_pair in obj_pairs:
			output = utils.are_touching(*obj_pair)
			self.assertFalse(output)


if __name__ == '__main__':
	unittest.main()