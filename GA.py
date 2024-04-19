import random
import threading
from fitness import determine_fitness



def calculate_fitness(individual, carerList):
    fitness = determine_fitness(individual, carerList)
    return fitness

# Function to generate a random individual
def generate_individual(n, names, shifts_per_day):
    individual = []
    for day in range(n):
        shifts = random.choices(names, k = shifts_per_day)
        individual.append(shifts)
    return individual

# Function to perform crossover between two individuals
def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Function to perform mutation on an individual
def mutate(individual, mutation_rate, names):
    mutated_individual = []
    for bit in individual:
        if random.random() < mutation_rate:
            name = random.choice(names)
            mutated_individual.append(name)
        else:
            mutated_individual.append(bit)
    return mutated_individual

# Function to run genetic algorithm for a single array
def run_genetic_algorithm(population_size, n, carerList, mutation_rate, generations, shifts_per_day):
    names = carerList.get_carer_names()
    population = [generate_individual(n, names, shifts_per_day) for _ in range(population_size)]
    
    for _ in range(generations):
        # Evaluate fitness
        fitness_scores = [calculate_fitness(individual, carerList) for individual in population]
        
        # Select parents
        selected_parents = random.choices(population, weights=fitness_scores, k=2)
        # Perform crossover and mutation
        children = crossover(*selected_parents)
        mutated_children = [mutate(child, mutation_rate, names) for child in children]

        # Replace the least fit individuals
        population.extend(mutated_children)
        population = sorted(population, key=lambda ind: calculate_fitness(ind, carerList), reverse=True)[:population_size]

    best_individual = max(population, key=lambda ind: calculate_fitness(ind, carerList))
    return best_individual, calculate_fitness(best_individual, carerList)

# Function to run genetic algorithm concurrently for multiple arrays using threading
def run_concurrent_genetic_algorithm(population_size, n, carerList, mutation_rate, generations, num_arrays, shifts_per_day):
    results = []
    threads = []

    # Define worker function for each thread
    def worker():
        result = run_genetic_algorithm(population_size, n, carerList, mutation_rate, generations, shifts_per_day)
        results.append(result)

    # Create and start threads
    for _ in range(num_arrays):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
            
    return results