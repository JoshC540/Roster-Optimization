import matplotlib.pyplot as plt
import time
from GA import run_concurrent_genetic_algorithm

# Generates a graph of number of generations against fitness, times also tracked so thet can be used in place of fitness
def plot_generations_vs_fitness(population_size, n, patientGraph, mutation_rate, shifts_per_day, shifts_per_night):
    generations = [10, 100, 250, 500, 1000, 2500, 5000, 7500, 10000]
    times = []
    fitnesses = []
    for generation in generations:
        start_time_graph = time.time()
        results = run_concurrent_genetic_algorithm(population_size, n, patientGraph, mutation_rate, generation, 1, shifts_per_day, shifts_per_night)
        end_time_graph = time.time()
        execution_time_graph = end_time_graph - start_time_graph
        times.append(execution_time_graph)
        for i, (best_individual, fitness) in enumerate(results):
            fitnesses.append(fitness)

    plt.plot(generations, fitnesses, marker='o', label='Genetic Algorithm')
    plt.title('Genetic Algorithm Fitness vs Generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()
    
# Generates a graph of number of population against fitness, times also tracked so thet can be used in place of fitness
def plot_populations_vs_fitness(generations, n, patientGraph, mutation_rate, shifts_per_day, shifts_per_night):
    populations = [10, 100, 250, 500, 750, 1000, 1250, 1500]
    times = []
    fitnesses = []
    for population_size in populations:
        start_time_graph = time.time()
        results = run_concurrent_genetic_algorithm(population_size, n, patientGraph, mutation_rate, generations, 1, shifts_per_day, shifts_per_night)
        end_time_graph = time.time()
        execution_time_graph = end_time_graph - start_time_graph
        times.append(execution_time_graph)
        for i, (best_individual, fitness) in enumerate(results):
            fitnesses.append(fitness)

    plt.plot(populations, fitnesses, marker='o', label='Genetic Algorithm')
    plt.title('Genetic Algorithm Fitness vs Populations')
    plt.xlabel('Populations')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()

# Generates a graph of number of mutation rate against fitness, times also tracked so thet can be used in place of fitness
def plot_mutation_rates_vs_fitness(population_size, generations, n, patientGraph, shifts_per_day, shifts_per_night):
    mutation_rates = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 0.9]
    times = []
    fitnesses = []
    for mutation_rate in mutation_rates:
        start_time_graph = time.time()
        results = run_concurrent_genetic_algorithm(population_size, n, patientGraph, mutation_rate, generations, 1, shifts_per_day, shifts_per_night)
        end_time_graph = time.time()
        execution_time_graph = end_time_graph - start_time_graph
        times.append(execution_time_graph)
        for i, (best_individual, fitness) in enumerate(results):
            fitnesses.append(fitness)

    plt.plot(mutation_rates, fitnesses, marker='o', label='Genetic Algorithm')
    plt.title('Genetic Algorithm Fitness vs Mutation Rates')
    plt.xlabel('Mutation Rates')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()