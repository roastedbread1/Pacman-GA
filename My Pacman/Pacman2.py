from Game import *
from Simulation1 import *
from GAPopInit import *
from Crossover import *
from Mutation import *

# hyperparameters
max_generation = 250
basically_the_same_threshold = 1e-5
game_length = 60 * 60       # also as chromosome_length, gene_count
input_delay = 10


def early_stop_check(n_last_fitnesses):
    c = len(n_last_fitnesses) - 1
    sum = 0
    for i in range(c):
        sum += abs(n_last_fitnesses[i+1] - n_last_fitnesses[i])
    return sum / c < basically_the_same_threshold

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


def pacman_ga(populations, mating_times, mutation_probability, tournament_size):

    pop_fitnesses = calculate_population_fitness(populations)

    mating_pool_size = len(populations)
    mating_pool = random.choices(
        populations, weights=pop_fitnesses, k=mating_pool_size)
    
    children = []
    for i in range(mating_times):
        parent1 = tournament_selection(
            mating_pool, pop_fitnesses, tournament_size)
        parent2 = tournament_selection(
            mating_pool, pop_fitnesses, tournament_size)

        child1, child2 = crossover(parent1, parent2)
        children.append(child1)
        children.append(child2)

    for i in range(len(children)):
        children[i] = mutation(children[i], mutation_probability)

    combined_population = populations + children
    children_fitnesses = calculate_population_fitness(children)

    combined_fitnesses = pop_fitnesses + children_fitnesses
    # combined_fitnesses = calculate_population_fitness(combined_population)

    sorted_individuals = sorted(
        zip(combined_population, combined_fitnesses), key=lambda x: x[1], reverse=True)

    average_fitness = sum(combined_fitnesses) / len(combined_fitnesses)
    max_fitness = sorted_individuals[0][1]

    print(f'generation max fitness {max_fitness}')
    print(f'generation avg fitness {average_fitness}')

    new_populations = [individual for individual,
                       fitness in sorted_individuals[:len(populations)]]

    return new_populations, (max_fitness, average_fitness)


class SimulationParams:

    def __init__(self, game_length, pop_count, mating_times, mutation_probability, tournament_size, patience, max_generation):
        self.game_length = game_length
        self.pop_count = pop_count
        self.mating_times = mating_times
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size
        self.patience = patience
        self.max_generation = max_generation
        
    def __repr__(self) -> str:
        return f'Params({self.game_length}, {self.pop_count}, {self.mating_times}, {self.mutation_probability}, {self.tournament_size}, {self.patience}, {self.max_generation})'



def simulate(params):

    populations = create_init_population_bin(params.game_length, params.pop_count)

    generation_history = []

    for i in range(params.max_generation):
        print(f'generation {i+1}')
        populations, gen_result = pacman_ga(populations, params.mating_times, params.mutation_probability, params.tournament_size)
        generation_history.append(gen_result)

        # early stop if it's getting stagnant
        if (i >= params.patience) and early_stop_check([res[1] for res in generation_history[-params.patience:]]):
            print('early stopped')
            break
        print('')

    print('done')


def simulate_writefile(params):
    report = open(f'{repr(params)}.txt', 'w')
    report.write(repr(params))
    report.write('\n')

    populations = create_init_population_bin(params.game_length, params.pop_count)
    generation_history = []

    for i in range(params.max_generation):
        print(f'generation {i+1}')
        report.write(f'gen {i}\n')

        populations, gen_result = pacman_ga(populations, params.mating_times, params.mutation_probability, params.tournament_size)
        generation_history.append(gen_result)

        report.write(f'max: {gen_result[0]}\n')
        report.write(f'avg: {gen_result[1]}\n')
        report.write('best individu: ')
        report.write(str(populations[0]))
        report.write('\n')

        # early stop if it's getting stagnant
        if (i >= params.patience) and early_stop_check([res[1] for res in generation_history[-params.patience:]]):
            print('early stopped')
            break
        print('')

    print('done')
    report.close()

# MAIN #

pop_count_list = [10, 20, 30, 100]
mating_times_list = [10, 15, 20, 50]
mutation_probability_list = [0.05, 0.1, 0.15, 0.75]
tournament_size_list = [3, 5]

for pc in pop_count_list:
    for mt in mating_times_list:
        for mp in mutation_probability_list:
            for ts in tournament_size_list:

                params = SimulationParams(
                    game_length = 1200,
                    pop_count = pc,
                    mating_times = mt,
                    mutation_probability = mp,
                    tournament_size = ts,
                    patience = 5,
                    max_generation = 250
                )
                simulate_writefile(params)
            
            

# params = SimulationParams(
#     game_length = 16,
#     pop_count = 2,
#     mating_times = 5,
#     mutation_probability = 0.1,
#     tournament_size = 2,
#     patience = 2,
#     max_generation = 250
# )
# simulate(params)



