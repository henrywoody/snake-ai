import random
import math
from holland import Evolver, library
from board import Board


def fitness_function(genome):
	board = Board(400, 300, num_food=25, snake_genome=genome, animation_on=False)
	length, time = board.run(time_limit=200, time_bonus=100, max_time=2000)
	score = length * 100 + time
	return score

genome_params = {
	"eye_angles": {
		"type": "[float]",
		"size": 2,
		"max": math.pi * 2,
		"min": 0,
		"initial_distribution": lambda: random.random() * math.pi * 2,
		"crossover_function": library.get_uniform_crossover_function(),
		"mutation_function": library.get_gaussian_mutation_function(sigma=1),
		"mutation_rate": 0.01
	},
	"w1": {
		"type": "[float]",
		"size": 15 * 15,
		"initial_distribution": lambda: random.random() * 200 - 100,
		"crossover_function": library.get_point_crossover_function(n_crossover_points=3),
		"mutation_function": library.get_gaussian_mutation_function(sigma=50),
		"mutation_rate": 0.15

	},
	"w2": {
		"type": "[float]",
		"size": 5 * 15,
		"initial_distribution": lambda: random.random() * 200 - 100,
		"crossover_function": library.get_point_crossover_function(n_crossover_points=3),
		"mutation_function": library.get_gaussian_mutation_function(sigma=50),
		"mutation_rate": 0.15
	}
}

selection_strategy = {
	"pool": {
		"top": 15,
		"bottom": 2,
		"random": 2
	},
	"parents": {
		"weighting_function": library.get_polynomial_weighting_function(power=1.5)
	}
}

evolver = Evolver(fitness_function, genome_params, selection_strategy)


storage_options = {
	"fitness": {
		"should_record_fitness": True,
		"format": "csv",
		"file_name": "fitness.csv",
		"path": "./results/"
	},
	"genomes": {
		"should_record_on_interrupt": True,
		"format": "json",
		"file_name": "genomes.json",
		"path": "./results/",
		"top": 10
	}
}

final_pop = evolver.evolve(
	generation_params={"population_size": 1000, "n_elite": 1},
	storage_options=storage_options,
	stop_conditions={"n_generations": math.inf}
)