import sys
import numpy as np
import random
import pygame
from pygame.locals import *

from snake import Snake
from food import Food
import utils


class Board:
	def __init__(self, width, height, snake_genome=[0,0], num_food=1, seed=2188357, animation_on=True):
		self.width = width
		self.height = height
		self.animation_on = animation_on
		self.color = (34, 139, 34)

		random.seed(seed)

		self.snake = self.spawn_snake(genome=snake_genome)

		self.num_food = num_food
		self.foods = self.spawn_food(num_food)

		if self.animation_on:
			pygame.init()
			self.fps_clock = pygame.time.Clock()
			self.fps = 60
			self.surface = pygame.display.set_mode((self.width, self.height))
			pygame.display.set_caption('Snake')

	def run(self, time_limit=np.inf, time_bonus=0, max_time=np.inf):
		time_passed = 0
		while self.snake.is_alive and time_passed < min(time_limit, max_time):
			starting_length = len(self.snake.body)
			self.update()
			food_eaten = len(self.snake.body) - starting_length
			time_limit += food_eaten * time_bonus

			if self.animation_on:
				self.update_animation()
			
			time_passed += 1

		return len(self.snake.body), time_passed, self.snake.is_alive

	def update(self):
		self.snake.update(self.foods)

		next_foods = []
		for food in self.foods:
			if utils.are_touching(self.snake.body[0], food):
				self.snake.grow()
			else:
				next_foods.append(food)
		self.foods = next_foods
		if len(self.foods) != self.num_food:
			self.foods += self.spawn_food(self.num_food - len(self.foods))

	def spawn_snake(self, genome):
		init_snake_position = [self.width/2, self.height/2]
		init_snake_direction = 0
		return Snake(init_snake_position, init_snake_direction, genome=genome)

	def spawn_food(self, num):
		return [Food(self.get_random_position()) for _ in range(num)]

	def update_animation(self):
		self.draw()
		self.check_quit()
		self.fps_clock.tick(self.fps)

	def draw(self):
		self.surface.fill(self.color)
		
		self.snake.draw(self.surface)
		for food in self.foods:
			food.draw(self.surface)

		pygame.display.update()

	def get_random_position(self):
		x = random.random() * self.width
		y = random.random() * self.height
		return x,y

	def check_quit(self):
		for event in pygame.event.get(QUIT):
			self.terminate()
		for event in pygame.event.get(KEYUP):
			if event.key == K_ESCAPE:
				self.terminate()
			pygame.event.post(event)

	def terminate(self):
		pygame.quit()
		sys.exit()