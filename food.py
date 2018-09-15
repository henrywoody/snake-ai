import pygame
from mixins import DrawableMixin


class Food(DrawableMixin):
	def __init__(self, position, size=3):
		self.position = position
		self.size = size
		self.color = (255, 255, 0)
		self.visual_encoding: [0,1]
