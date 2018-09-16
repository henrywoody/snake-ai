import math
import numpy as np
import pygame
from functools import reduce

from mixins import DrawableMixin
import utils

SNAKE_SPEED = 0.5


class Snake:
	def __init__(self, init_position, init_direction, genome=[0,0]):
		self.body = [self.BodyPiece(init_position)]
		self.direction = init_direction
		self.speed = SNAKE_SPEED
		self.turn_angle1 = genome[0]
		self.turn_angle2 = genome[1]
		self.eye_angles = [0, self.turn_angle1, -self.turn_angle1, self.turn_angle2, -self.turn_angle2]
		self.brain = self.Brain(genome[2:])
		self.is_alive = True

		if self.turn_angle1 > np.pi or self.turn_angle2 > np.pi: self.is_alive = False

	def update(self, other_objects):
		vision = self.look(other_objects)
		decision = self.decide(vision)
		self.act(decision)
		self.move()

	def look(self, other_objects):
		visuals = [None for eye in self.eye_angles]
		head = self.body[0]

		for other_object in other_objects + self.body[2:]:
			distance = utils.calc_distance(head.position, other_object.position)
			angle = utils.calc_angle(head.position, other_object.position)
			view_angle_freedom = math.asin(other_object.size / distance) if distance >= other_object.size else 2*np.pi

			for i, eye_angle in enumerate(self.eye_angles):
				if visuals[i] and distance > visuals[i][2]: continue

				view_angle = (eye_angle + self.direction) % (2*np.pi)
				if abs(view_angle - angle) <= view_angle_freedom:
					visuals[i] = other_object.visual_encoding + [distance]

		return reduce(lambda a,x: a + x if x is not None else a + [0,0,0], visuals, [])

	def decide(self, information):
		decision_vector = self.brain.forward(np.array(information))
		return decision_vector.argmax()

	def act(self, decision):
		if decision == 0:
			self.turn(-self.turn_angle1)
		elif decision == 1:
			self.turn(-self.turn_angle2)
		elif decision == 2:
			self.turn(self.turn_angle1)
		elif decision == 3:
			self.turn(self.turn_angle2)

	def grow(self):
		position = self.body[-1].history[0]
		self.body.append(self.BodyPiece(position))

	def turn(self, angle):
		self.direction = (self.direction + angle) % (2*np.pi)

	def move(self):
		next_position = self.calc_next_position()
		head_piece = self.body[0]
		head_piece.move_to(next_position)

		for i in range(1, len(self.body)):
			self.body[i].move_to(self.body[i-1].history[0])

	def calc_next_position(self):
		head_piece = self.body[0]
		next_x = head_piece.position[0] + self.speed * np.cos(self.direction)
		next_y = head_piece.position[1] + self.speed * np.sin(self.direction)
		return [next_x, next_y]

	def is_touching_tail(self):
		head = self.body[0]
		for body_piece in self.body[2:]: #skipping first piece because they _should_ be touching
			if utils.are_touching(head, body_piece):
				return True
		return False

	def draw(self, surface):
		for body_piece in self.body:
			body_piece.draw(surface)

	class BodyPiece(DrawableMixin):
		def __init__(self, position):
			self.position = position[:]
			self.size = 5
			self.color = (0, 0, 0)
			self.visual_encoding = [1,0]
			self.history = [position[:]]
			self.max_history = int(self.size * 2 / SNAKE_SPEED) # to get the piece spacing correct

		def move_to(self, position):
			self.position = position
			self.update_history(self.position)

		def update_history(self, position):
			self.history.append(position[:])
			if len(self.history) > self.max_history:
				self.history = self.history[-self.max_history:]

	class Brain:
		def __init__(self, layers):
			self.layers = layers
			if not self.layers:
				self.layers = self.generate_random_layers()

		def generate_random_layers(self):
			dimensions = [15, 15, 5] #15 comes from len(snake.eye_angles) * len(visual_encoding)
			w1 = np.random.rand(dimensions[1], dimensions[0])
			w2 = np.random.rand(dimensions[2], dimensions[1])
			return w1,w2

		def sigmoid(self, x):
			return 1 / (1 + np.exp(-x))

		def forward(self, vector):
			for layer in self.layers:
				vector = self.sigmoid(np.matmul(layer, vector))
			return vector

