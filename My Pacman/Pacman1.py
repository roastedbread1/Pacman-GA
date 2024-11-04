from Game import *
from Simulation1 import *
from GAPopInit import *
from Crossover import *
from Selection import *
from Mutation import *

input_delay = 10

# parameters
game_length = 60            # also as chromosome_length, gene_count
pop_count = 10              # population count for each generation
mating_pool_size = 10       # how many individuals are probable to crossover
# how many times crossover attempted. child_count = 2 * mating_times
mating_times = 5
mutation_probability = 0.5  # probability of mutation
tournament_entrant_count = 2      # how many entree in a tournament


# one loop
populations = create_init_population_bin(game_length, pop_count)


def tournament_selection(populations, pop_fitnesses, tournament_size):
    tournament = random.sample(
        list(zip(populations, pop_fitnesses)), tournament_size)
    # Pilih yang dengan fitness terbaik
    winner = max(tournament, key=lambda x: x[1])
    return winner[0]


def calculate_population_fitness(population):
    fitnesses = []
    i = 0
    for individual in population:
        game = Game()  # Inisialisasi game
        inputs = chromosome_bin_iterator(individual)
        game.injectInput(inputs, input_delay)
        game.run()

        points = game.pacman.points
        time_left = 0 if game.pacman.lives == 0 else game_length - \
            game.frameElapsed // input_delay
        fitness = calculate_fitness(points, time_left)

        print(f'Individual {i+1} Fitness: {fitness}')
        i += 1
        fitnesses.append(fitness)
    return fitnesses


def pacman_ga(populations):
    pop_fitnesses = calculate_population_fitness(populations)

    mating_pool_size = len(populations)
    mating_pool = random.choices(
        populations, weights=pop_fitnesses, k=mating_pool_size)

    children = []
    for i in range(mating_times):
        parent1 = tournament_selection(
            mating_pool, pop_fitnesses, tournament_size=3)
        parent2 = tournament_selection(
            mating_pool, pop_fitnesses, tournament_size=3)

        child1, child2 = crossover(parent1, parent2)
        children.append(child1)
        children.append(child2)

    # for i in range(len(children)):
    #     if random.random() < mutation_probability:
    #         children[i] = mutation(children[i], mutation_probability)

    for i in range(len(children)):
        children[i] = mutation(children[i], mutation_probability)

    combined_population = populations + children
    children_fitnesses = calculate_population_fitness(children)

    combined_fitnesses = pop_fitnesses + children_fitnesses
    # combined_fitnesses = calculate_population_fitness(combined_population)

    sorted_individuals = sorted(
        zip(combined_population, combined_fitnesses), key=lambda x: x[1], reverse=True)

    new_populations = [individual for individual,
                       fitness in sorted_individuals[:pop_count]]

    return new_populations


for i in range(10):
    print(f'generation {i+1}')
    populations = pacman_ga(populations)
    print('')

# end loop
