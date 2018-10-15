# Snake AI

An artificially intelligent player for Snake. The snake's brain is a neural network and is improved via the genetic algorithm.

Written in Python using Pygame for graphics/user interaction. Evolution handled by [Holland](https://github.com/lambdalife/holland).

![Sample](https://github.com/henrywoody/snake-ai/blob/master/gallery/sample2.mov)

See the [gallery](https://github.com/henrywoody/snake-ai/blob/master/gallery) for more sample runs, corresponding genomes are in [samples](https://github.com/henrywoody/snake-ai/blob/master/samples).

## Snake Anatomy

Snakes have 5 eyes and can see the closest object that falls along the straight line starting at the snake's head at the angle of the eye..

Snakes brains are neural nets with one hidden layer, 15 input nodes, and 5 output nodes. The 15 inputs correspond to the inputs of the eyes. Each eye receives 3 inputs—2 are the visual encoding of the object, and the final is the distance from the snake's head to the object. Each of the 5 output nodes correspond to turning in the direction of one of the snake's eyes (one eye points forward so this is just not turning).

## Setup

If running evolution, create a folder within this project folder called `results`—this is where fitness statistics and genomes will be stored.

## Running

Run `python3 run.py` to view the best individual from the most recent run of evolution.

## Evolving

Run `python3 evolution.py` to start evolution.