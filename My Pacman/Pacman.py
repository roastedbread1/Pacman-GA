'''
This is not the file to run simulated annealing. Please run the Simulate.py file
'''


from Game import *
from GAPopInit import *

input_delay = 10

game_length = 60 * 60   # also as chromosome_length, gene_count
pop_count = 1

populations = create_init_population_bin(game_length, pop_count)
print(populations[0])

inputs = chromosome_bin_iterator(populations[0])

game = Game()
game.injectInput(inputs, input_delay)
game.run()

points = game.pacman.points
time_left = 0 if game.pacman.lives == 0 else len(inputs) - game.frameElapsed // input_delay 

print("points:")
print(points)
print("time_left:")
print(time_left)
print("fitness:")
print(calculate_fitness(points, time_left))