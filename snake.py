import math
import numpy as np
import pygame

from mixins import DrawableMixin
import utils

SNAKE_SPEED = 0.5


class Snake:
	def __init__(self, position, direction, brain_layers=None):
		self.direction = direction
		self.speed = SNAKE_SPEED
		self.body = [self.BodyPiece(position)]
		self.eye_angles = [0]
		self.is_alive = True

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

		return [visual if visual is not None else [0,0,0] for visual in visuals]

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







