import numpy as np
import random
from GAPopInit import *

def crossover(n, parent1, parent2):
    li = [random.randint(0, 1<<32-1) for i in range(n)]
    child1 = [0]*n
    child2 = [0]*n
    for i in range(n):
        child1[i] = (parent1[i] & ~li[i]) | (parent2[i] & li[i])
        child2[i] = (parent2[i] & ~li[i]) | (parent1[i] & li[i])
    return child1, child2

game_length = 60 * 60   # also as chromosome_length, gene_count
pop_count = 2

populations = create_init_population_bin(game_length, pop_count)

print(len(populations[0]), len(populations[1]))

# print(crossover(225, populations[0], populations[1]))
