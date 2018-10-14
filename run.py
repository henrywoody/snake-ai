import random
import numpy as np
import json

from board import Board

if __name__ == '__main__':
	with open('results/genomes.json', 'r') as f:
		all_results = json.loads(f.readline()).get("results")
		best_result = all_results[-1]
		snake_genome = best_result[1]

	board = Board(400, 300, num_food=25, snake_genome=snake_genome, seed=random.random())
	board.run()