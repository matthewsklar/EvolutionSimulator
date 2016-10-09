class Genome(object):
    def __init__(self, fitness, weights):
        # Fitness score of the genome
        self.fitness = fitness

        # Weights in the genome
        self.weights = weights


class GeneticAlgorithm(object):
    # Current generation
    generation = 0

    # Population of chromosomes
    population = []

    # Amount of weights per chromosome
    chromo_length = 0

    # Net fitness of the population
    net_fitness = 0

    # Best fitness of the population
    best_fitness = 0

    # Average fitness of the population
    average_fitness = 0

    # Worst fitness of the population
    worst_fitness = 0

    def __init__(self, pop_size, mutation_rate, crossover_rate, num_weights):
        # Size of the population
        self.population_size = pop_size

        # Probability that chromosome bits will mutate
        self.mutation_rate = mutation_rate

        # Probability of chromosomes crossing over bits
        self.crossover_rate = crossover_rate

        # Amount of weights
        self.num_weights = num_weights
