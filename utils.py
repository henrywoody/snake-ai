import math
import numpy as np

def calc_distance(a, b):
	dx = b[0] - a[0]
	dy = b[1] - a[1]
	return math.sqrt(dx**2 + dy**2)

def calc_angle(a, b):
	dx = b[0] - a[0]
	dy = b[1] - a[1]
	return math.atan2(dy, dx) % (2*np.pi)

def are_touching(a, b):
	distance = calc_distance(a.position, b.position)
	min_touching_distance = a.size + b.size
	return distance <= min_touching_distance