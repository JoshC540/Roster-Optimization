import random
import threading
from fitness import determine_fitness

# Define Reward Machine parameters
reward_machine = {
    'states': ['A', 'B', 'C'],  # Example states
    'actions': ['Crossover', 'Mutate'],  # Example actions
    'transitions': {
        'A': {'Crossover': 'B', 'Mutate': 'C'},
        'B': {'Crossover': 'C', 'Mutate': 'A'},
        'C': {'Crossover': 'A', 'Mutate': 'B'}
    },
    'rewards': {
        'A': {'Crossover': 10, 'Mutate': 5},
        'B': {'Crossover': 8, 'Mutate': 7},
        'C': {'Crossover': 6, 'Mutate': 3}
    }
}

def calculate_fitness(individual, carerList):
    fitness = determine_fitness(individual, carerList)
    return fitness

# Function to generate a random individual
def generate_individual(n, names, carerList, shifts_per_day, shifts_per_night):
    individual = []
    
    for day in range(n):
        day_carers = carerList.get_day_carers()
        night_carers = carerList.get_night_carers()
        shifts = []
        day_shifts = random.sample(day_carers, k=shifts_per_day)
        for name in day_shifts:
            shifts.append(name)
            if name in night_carers:
                night_carers.remove(name)
                
        night_shifts = random.sample(night_carers, k=shifts_per_night)
        for name in night_shifts:
            shifts.append(name)
        
        individual.append(shifts)
        
    return individual

# Function to perform crossover between two individuals
def crossover(parent1, parent2, current_state, population):
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

def calculate_reward(state, action):
    return reward_machine['rewards'][state][action]

def select_action(state):
    possible_actions = reward_machine['actions']
    return random.choice(possible_actions)

def update_state(state, action):
    return reward_machine['transitions'][state][action]

def run_reward_machine(population_size, mutation_rate, n, carerList, generations, shifts_per_day, shifts_per_night):
    names = carerList.get_carer_names()
    population = [generate_individual(n, names, carerList, shifts_per_day, shifts_per_night) for _ in range(population_size)]
    current_state = 'A'

    for _ in range(generations):
        percent = (_ / generations) * 100
        print(f"{percent}%")
        for i, individual in enumerate(population):
            action = select_action(current_state)
            next_state = update_state(current_state, action)
            reward = calculate_reward(current_state, action)
            
            fitness = calculate_fitness(individual, carerList)
            
            # Update population based on rewards
            if reward > 0 and fitness > 1:  # If the action is rewarding
                if action == 'Mutate':
                    population[i] = mutate(individual, mutation_rate, names)
                else:
                    population[i], _ = crossover(individual, random.choice(population), current_state, population)

        current_state = next_state  # Update the current state

    best_individual = max(population, key=lambda ind: calculate_fitness(ind, carerList))
    return best_individual, calculate_fitness(best_individual, carerList)
