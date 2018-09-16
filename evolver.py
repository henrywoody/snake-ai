import time
import random
import numpy as np
from functools import reduce

from board import Board

class Evolver:
	def __init__(self, generations, pop_per_generation, random_per_generation):
		self.generations = generations
		self.pop_per_generation = pop_per_generation
		self.random_per_generation = random_per_generation

	def evolve(self, gene_pool):
		generation_num = 0
		max_scores = []
		while generation_num < self.generations:
			try:
				start_time = time.time()
				results = self.evaluate_population(gene_pool)
				max_score = max([r[0] for r in results])
				max_scores.append(max_score)
				print('Generation {}:\r\n\tMax score: {}, Time: {}'.format(generation_num, max_score, round(time.time() - start_time, 2)))
				gene_pool = self.generate_next_generation(results)
				generation_num += 1
			except:
				# raise
				break
		return sorted(results, key=lambda x: x[0], reverse=True), max_scores

	def evaluate_population(self, gene_pool):
		results = []
		for genome in gene_pool:
			board = Board(400, 300, num_food=25, snake_genome=genome, animation_on=False)
			length, time = board.run(time_limit=200, time_bonus=100, max_time=2000)
			score = length * 100 + time
			results.append([score, genome])
		return results

	def generate_next_generation(self, results):
		weight = lambda x: x**1.2
		total_score = reduce(lambda a,x: a + weight(x[0]), results, 0)
		scores, genes = zip(*results)
		probabilities = [weight(score) / total_score for score in scores]

		next_generation = []
		for _ in range(self.pop_per_generation - self.random_per_generation):
			parent_indices = np.random.choice(list(range(len(genes))), size=2, replace=False, p=probabilities)
			child = self.breed(genes[parent_indices[0]], genes[parent_indices[1]])
			next_generation.append(child)

		next_generation += self.generate_random_genes(self.random_per_generation)

		return next_generation

	def generate_random_genes(self, num):
		gene_pool = []
		for _ in range(num):
			turn_angles = [random.random() * np.pi for _ in range(2)]
			brain_weights = [random.random() * 200 - 100 for _ in range(15 * 15 + 15 * 5)]
			gene_pool.append(turn_angles + brain_weights)
		return gene_pool

	def breed(self, a, b):
		return self.mutate(self.crossover(a, b))

	def crossover(self, a, b):
		genome = []
		for i in range(len(a)):
			if random.random() < 0.5:
				genome.append(a[i])
			else:
				genome.append(b[i])
		return genome

	def mutate(self, genome):
		new_genome = genome[:]
		for i in range(len(new_genome)):
			new_genome[i] *= random.random() * 4 - 2
		return new_genome


if __name__ == '__main__':
	pop = 500
	evolver = Evolver(1000, pop, pop // 10)
	init_gene_pool = evolver.generate_random_genes(pop)
	results, max_scores = evolver.evolve(init_gene_pool)

	print(max_scores)

	with open('brains.out', 'w') as f:
		for result in results:
			f.write(str(result[1]) + '\r\n')
