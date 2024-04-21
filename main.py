from carer import Carer
from carerList import CarerList
from GA import run_concurrent_genetic_algorithm
from RM import run_reward_machine
import time
import matplotlib.pyplot as plt

# Record the start time
start_time = time.time()

# Your program code goes here

patientOne = CarerList("John")



mary = Carer("mary", 0, 0, [0, 0, 0, 0, 0, 0, 0], [], [], True, False)
patientOne.add_to_list(mary)

jane = Carer("jane", 1, 1, [1, 0, 1, -1, 1, -1, 0], [], [], False, True)
patientOne.add_to_list(jane)

sue = Carer("sue", 0, 0, [1, -1, -1, 0, 0, 0, 0], [], [], True, True)
patientOne.add_to_list(sue)

beth = Carer("beth", 2, 1, [1, 1, 1, 0, 0, 0, 0], [], [], True, False)
patientOne.add_to_list(beth)

tom = Carer("tom", 2, 0, [0, 0, 0, 0, -1, -1, -1], [], [], True, True)
patientOne.add_to_list(tom)

jim = Carer("jim", 1, 2, [0, 0, 0, 0, 1, 1, 1], [], [], True, True)
patientOne.add_to_list(jim)

"""
tim = Carer("tim", 2, 0, [0, 0, 0, 0, 0, -1, -1], [], [], True, True)
patientOne.add_to_list(tim)

harry = Carer("harry", 0, 0, [0, 0, 0, 0, 0, -1, -1], [], [], True, False)
patientOne.add_to_list(harry)

megan = Carer("megan", 0, 0, [0, 0, 0, 0, 0, 0, 0], [], [], True, True)
patientOne.add_to_list(megan)

albert = Carer("albert", 0, 0, [0, 0, 0, 0, 0, 0, 0], [], [], False, True)
patientOne.add_to_list(albert)
"""




#print("Testing")
#print(jim.name, jim.days)


num_of_weeks = 6
population_size = 1000
n = 7 * num_of_weeks  # Length of the array
mutation_rate = 0.01
generations = 10000
shifts_per_day = 1
shifts_per_night = 1

num_arrays = 1  # Number of arrays to generate concurrently

#results, best = run_reward_machine(population_size, mutation_rate, n, patientOne, generations, shifts_per_day, shifts_per_night)
#print(results)
#print(best)

"""
results = run_concurrent_genetic_algorithm(population_size, n, patientOne, mutation_rate, generations, num_arrays, shifts_per_day, shifts_per_night)
print(results)
for i, (best_individual, fitness) in enumerate(results):
    print(f"Best individual {i + 1}: {best_individual}, Fitness: {fitness}")

best_overall_individual, best_overall_fitness = max(results, key=lambda x: x[1])
print(f"\n\nBest overall individual: {best_overall_individual}, Fitness: {best_overall_fitness}")
"""

"""
Graphing Time vs Fitness
"""
generations = [10, 100, 250, 500, 1000, 2500, 5000, 7500, 10000]
times = []
fitnesses = []
for generation in generations:
    start_time_graph = time.time()
    
    results = run_concurrent_genetic_algorithm(population_size, n, patientOne, mutation_rate, generation, num_arrays, shifts_per_day, shifts_per_night)
    
    end_time_graph = time.time()
    execution_time_graph = end_time_graph - start_time_graph
    times.append(execution_time_graph)
    
    for i, (best_individual, fitness) in enumerate(results):
        fitnesses.append(fitness)

plt.plot(times, fitnesses, marker='o', label='Genetic Algorithm')

plt.title('Genetic Algorithm Fitness vs run time')
plt.xlabel('Runtime in seconds')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)

plt.show()


# Record the end time
end_time = time.time()

# Print the start and end times
print("Start Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
print("End Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))

# Calculate and print the total execution time
execution_time = end_time - start_time
print("Total Execution Time:", execution_time, "seconds")
