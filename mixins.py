import pygame


class DrawableMixin:
	def draw(self, surface):
		rounded_position = [int(round(x)) for x in self.position]
		pygame.draw.circle(surface, self.color, rounded_position, self.size)