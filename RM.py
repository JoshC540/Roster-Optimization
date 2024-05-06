import random
from fitness import determine_fitness


# I understand how it should work but making it work as intended was unable to be done in the time frame
# The tool doesn't use this and uses the genetic algorithm but this code remains as I wish to revist it and make it work
# Define Reward Machine parameters
# The big issue I had was figuring out how to convert my fitness scores which tell me how it is performing into actionable data
# The reward machine below does not generate good results but it is in the struture of a reward machine
# With more time this would have been made functional but 1 function generational tool was decided to be more important than 2 half working ones
reward_machine = {
    # List of possible states in the Reward Machine
    'states': ['A', 'B', 'C'],
    
    # List of possible actions that can be taken
    'actions': ['Crossover', 'Mutate'],
    
    # Dictionary defining transitions between states based on actions
    'transitions': {
        'A': {'Crossover': 'B', 'Mutate': 'C'},
        'B': {'Crossover': 'C', 'Mutate': 'A'},
        'C': {'Crossover': 'A', 'Mutate': 'B'}
    },
    
    # Dictionary specifying rewards associated with each state-action pair
    'rewards': {
        'A': {'Crossover': 10, 'Mutate': 5},
        'B': {'Crossover': 8, 'Mutate': 7},
        'C': {'Crossover': 6, 'Mutate': 3}
    }
}

# Calculate fitness score for an individual
def calculate_fitness(individual, carerList):
    fitness = determine_fitness(individual, carerList)
    return fitness

# Create random individual explained in the genetic algorithm code
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

# Perform crossover between two individuals
def crossover(parent1, parent2, current_state, population):
    crossover_point = random.randint(0, len(parent1) - 1)
    
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2


# Mutation on an individual
def mutate(individual, mutation_rate, names):
    mutated_individual = []
    for bit in individual:
        if random.random() < mutation_rate:
            name = random.choice(names)
            mutated_individual.append(name)
        else:
            mutated_individual.append(bit)
    return mutated_individual

# Gets reward of a that an action will have in this state
def calculate_reward(state, action):
    return reward_machine['rewards'][state][action]

# Select a random action from the choices
def select_action(state):
    possible_actions = reward_machine['actions']
    return random.choice(possible_actions)

# Change state based on new condition
def update_state(state, action):
    return reward_machine['transitions'][state][action]


"""
    I belive the core issue is that the fitness and rewards states aren't interacting so it is just hoping to stumble onto  success
    with more time I would find a way to make them interact in a meaningful way
"""
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
            
            # Calculate fitness
            fitness = calculate_fitness(individual, carerList)
            
            # Update population based on rewards
            if reward > 0 and fitness > 1:  # If the action is rewarding
                if action == 'Mutate':
                    population[i] = mutate(individual, mutation_rate, names)
                else:
                    population[i], _ = crossover(individual, random.choice(population), current_state, population)

        current_state = next_state  # Update the current state

    # Calculate fitness for the last generation
    for i, individual in enumerate(population):
        fitness = calculate_fitness(individual, carerList)
        population[i] = (individual, fitness)

    # Find the best individual based on fitness
    best_individual, best_fitness = max(population, key=lambda x: x[1])
    return best_individual, best_fitness
