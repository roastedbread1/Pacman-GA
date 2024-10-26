import random
from GAPopInit import *


def mutation(child, n):
    li = [random.randint(0, 1<<32-1) for i in range(n)]
    result = [0]*n
    for i in range(n):
        result[i] = child[i] ^ li[i]
    
    return result


game_length = 60 * 60   # also as chromosome_length, gene_count
pop_count = 1

populations = create_init_population_bin(game_length, pop_count)

print(mutation(populations[0], 225))
