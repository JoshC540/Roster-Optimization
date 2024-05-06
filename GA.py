import random
import threading
from fitness import determine_fitness

"""
    This is the genetic algorithm that makes the rosters, but it merely knows it has an array of arrays of names.
    Calculate fitness gives it the scores and it uses this to make the next generation
"""

# Gets the fitness score so we know if the roster is good or not
def calculate_fitness(individual, carerList):
    fitness = determine_fitness(individual, carerList)
    return fitness


"""
Generates a random individual, takes the number the following:
    n = number of days
    names = all of the carer names
    carerList = list of carer objects
    shifts_per_day = shifts per day, done this way so in the future work multiple days shifts can be had
    shifts_per_night = shifts per night, done this way so in the future work multiple night shifts can be had
 """
 
def generate_individual(n, names, carerList, shifts_per_day, shifts_per_night):
    individual = []
    
    for day in range(n):
        # Get only names take can do days
        day_carers = carerList.get_day_carers()
        # Get only names take can do nights
        night_carers = carerList.get_night_carers()
        shifts = []
        # Picks a number of random names from the elilbe carers for the dayshift equal to the shifts per day
        day_shifts = random.sample(day_carers, k = shifts_per_day)
        for name in day_shifts:
            shifts.append(name)
            # If they also do nights we remove them from that list temporarily
            if name in night_carers:
                night_carers.remove(name)
        
        # Picks a number of random names from the elilbe carers for the night shift equal to the shifts per night
        night_shifts = random.sample(night_carers, k = shifts_per_day)
        for name in night_shifts:
            shifts.append(name)
        
        # Add the days shifts to the individual 
        individual.append(shifts)
        
        #print(individual)
    return individual

# Preform crossover between the two parents
def crossover(parent1, parent2):
    # Select a random crossover point within the length of the individuals
    crossover_point = random.randint(0, len(parent1) - 1)
    # Create child1 by combining the first part of parent1 and the second part of parent2
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    # Create child2 by combining the first part of parent2 and the second part of parent1
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutating the roster
def mutate(individual, mutation_rate, names):
    mutated_individual = []
    # Iterate over each name in the individual
    for current_name in individual:
        # Check if a mutation should occur based on the mutation rate
        if random.random() < mutation_rate:
            # If a mutation occurs, replace the name with a random name from the list of names
            new_name = random.choice(names)
            mutated_individual.append(new_name)
        else:
            # If no mutation occurs, keep the name unchanged
            mutated_individual.append(current_name)
    return mutated_individual

# Function to run genetic algorithm for a single array
def run_genetic_algorithm(population_size, n, carerList, mutation_rate, generations, shifts_per_day, shifts_per_night):
    # Getting our list of names
    names = carerList.get_carer_names()
    # Make a number of individuals equal to the population size
    population = [generate_individual(n, names, carerList, shifts_per_day, shifts_per_night) for _ in range(population_size)]
    
    # Performs this loop for each generation passed in. 
    for _ in range(generations):
        # Tracking progress
        percent = (_/generations) * 100
        print(f"{percent}%")
        
        # Evaluate fitness for each individual of the population
        fitness_scores = [calculate_fitness(individual, carerList) for individual in population]
        #print(fitness_scores)
        
        # Select 2 parents randomly based on their fitness score.
        selected_parents = random.choices(population, weights=fitness_scores, k=2)
        
        # Perform crossover with the two parents to create children
        children = crossover(*selected_parents)
        
        # Perform mutation on the children
        # This allows us to explore the solution space more
        mutated_children = [mutate(child, mutation_rate, names) for child in children]

        # Add the mutated children
        population.extend(mutated_children)
        
        # Sort the population based on each individual's fitness score in descending order
        # The key argument specifies the function used to extract the fitness score
        # lambda ind: calculate_fitness(ind, carerList) calculates the fitness score for each individual
        # reverse=True sorts the population in descending order
        population = sorted(population, key=lambda ind: calculate_fitness(ind, carerList), reverse=True)[:population_size]

    # Gets the single best individual
    best_individual = max(population, key=lambda ind: calculate_fitness(ind, carerList))
    return best_individual, calculate_fitness(best_individual, carerList)

# Function to run genetic algorithm concurrently for multiple arrays using threading
# This is done in an attempt to add consistancy to the tool so that is any one fails to generate well we have fallover
# In the future this could be used to generate serval differnet rosters at once for different patients
def run_concurrent_genetic_algorithm(population_size, n, carerList, mutation_rate, generations, num_arrays, shifts_per_day, shifts_per_night):
    # Results are all of the results of each individual run
    results = []
    threads = []

    # Define worker function for each thread
    def worker():
        result = run_genetic_algorithm(population_size, n, carerList, mutation_rate, generations, shifts_per_day, shifts_per_night)
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