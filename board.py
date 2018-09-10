import pygame
from pygame.locals import *

from snake import Snake


class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.color = (34, 139, 34)

		init_snake_position = [self.width/2, self.height/2]
		init_snake_direction = 1.5
		self.snake = Snake(init_snake_position, init_snake_direction)
		self.foods = []

		pygame.init()
		self.fps_clock = pygame.time.Clock()
		self.fps = 60
		self.surface = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Snake')

	def run(self):
		while self.snake.is_alive:
			self.update()
			self.draw()

			self.check_quit()

			self.fps_clock.tick(self.fps)

	def update(self):
		self.snake.move()

	def draw(self):
		self.surface.fill(self.color)
		self.snake.draw(self.surface)
		pygame.display.update()

	def check_quit(self):
		for event in pygame.event.get():
			if event == QUIT:
				pygame.quit()
				sys.exit()