from math import sin, cos
from numpy import random

MUTATION_RATE = 0.1
ELITISM = 2

def main():
    pass

class Solution:
    def __init__(self, genome=None):
        '''
            Initialization. Generate random genome if not given.
        '''
        self.genome_length = 32
        if genome is None:
            genome = "".join([random.choice(("0", "1")) for _ in range(self.genome_length)])
        self.genome = genome

    def decode(self):
        '''
            returns a tuple of x and y value calculated from genome.
        '''
        def bin_range(binary):
            return int(binary, 2)/int("1"*len(binary), 2)
        x_range = (-5, 5)
        y_range = (-5, 5)
        x = x_range[0]+(x_range[1]-x_range[0])*bin_range(self.genome[:self.genome_length//2])
        y = y_range[0]+(y_range[1]-y_range[0])*bin_range(self.genome[self.genome_length//2:])
        return x, y

    def fitness(self):
        '''
            returns a fitness value based on its genome.
        '''
        x, y = self.decode()
        return ((cos(x)+sin(y))**2)/(x**2+y**2)


def populate(population, Organism, population_size) :
    population.extend([Organism() for _ in range(population_size)])
    population.sort(key=Organism.fitness, reverse=True)
    

# Parent Picking
def crossover_parents(population):
    parent1, parent2 = random.choice(population, size=2, replace=False)
    return parent1, parent2

# Crossover
def crossover(Organism, parent1, parent2) :
    div = random.randint(len(parent1.genome))
    genome1 = parent1.genome[:div]+parent2.genome[div:]
    genome2 = parent2.genome[:div]+parent1.genome[div:]
    child1 = Organism(genome1)
    child2 = Organism(genome2)
    return child1, child2

# Mutation
def mutated(genome) :
    '''
        returns a mutated genome randomly based on mutation rate.
    '''
    genome = list(genome)
    for idx, nucleotide in enumerate(genome):
        if random.uniform()<=MUTATION_RATE:
            if nucleotide=="0":
                genome[idx] = "1"
            else:
                genome[idx] = "0"
    genome = "".join(genome)
    return genome

def mutate_population(population):
    for entity in population:
        entity.genome = mutated(entity.genome)

# Generate next generation
def generate_next_generation(population):
    Organism = type(population[0])
    population_size = len(population)
    next_generation = []
    # elitism
    next_generation.extend(population[:ELITISM])
    
    while len(next_generation) < population_size:
        parent1, parent2 = crossover_parents(population)
        child1, child2 = crossover(Organism, parent1, parent2)
        next_generation.extend((child1,child2))

    mutate_population(next_generation)
    next_generation.sort(key=Organism.fitness, reverse=True)

    population[:] = next_generation



if __name__ == "__main":
    main()