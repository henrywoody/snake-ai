import numpy as np
import ast

from board import Board

if __name__ == '__main__':
	with open('brains.out', 'r') as f:
		snake_genome = ast.literal_eval(f.readline())

	board = Board(400, 300, num_food=25, snake_genome=snake_genome)
	board.run()