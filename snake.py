import numpy as np
import pygame


class Snake:
	def __init__(self, position, direction, brain_layers=None):
		self.direction = direction
		self.speed = 0.1
		self.body = [self.BodyPiece(position)]
		self.is_alive = True

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

	def draw(self, surface):
		for body_piece in self.body:
			body_piece.draw(surface)

	class BodyPiece:
		def __init__(self, position):
			self.position = position[:]
			self.history = [position[:]]
			self.max_history = 5
			self.visual_encoding = [1,0]
			self.size = 2
			self.color = (0, 0, 0)

		def move_to(self, position):
			self.position = position
			self.update_history(self.position)

		def update_history(self, position):
			self.history.append(position[:])
			if len(self.history) > self.max_history:
				self.history = self.history[-self.max_history:]

		def draw(self, surface):
			rounded_position = [int(round(x)) for x in self.position]
			pygame.draw.circle(surface, self.color, rounded_position, self.size)