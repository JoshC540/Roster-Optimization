from carer import Carer
from carerList import CarerList
from GA import run_concurrent_genetic_algorithm

patientOne = CarerList("John")



mary = Carer("mary", 0, 0, [0, 0, 0, 0, 0, 0, 0], [], 0, 0, [], True, True)
patientOne.add_to_list(mary)

jane = Carer("jane", 1, 1, [1, 0, 1, -1, 1, -1, 0], [], 0, 0, [], True, True)
patientOne.add_to_list(jane)

sue = Carer("sue", 0, 0, [1, -1, -1, 0, 0, 0, 0], [], 0, 0, [], True, False)
patientOne.add_to_list(sue)

beth = Carer("beth", 2, 1, [1, 1, 1, 0, 0, 0, 0], [], 0, 0, [], False, True)
patientOne.add_to_list(beth)

tom = Carer("tom", 2, 0, [0, 0, 0, 0, -1, -1, -1], [], 0, 0, [], True, False)
patientOne.add_to_list(tom)

jim = Carer("jim", 1, 2, [0, 0, 0, 0, 1, 1, 1], [], 0, 0, [], False, True)
patientOne.add_to_list(jim)

tim = Carer("tim", 0, 0, [0, 0, 0, 0, 0, -1, -1], [], 0, 0, [], False, True)
patientOne.add_to_list(tim)





#print("Testing")
#print(jim.name, jim.days)


num_of_weeks = 6
population_size = 100
n = 7 * num_of_weeks  # Length of the array
mutation_rate = 0.01
generations = 10000
shifts_per_day = 2

num_arrays = 20  # Number of arrays to generate concurrently


results = run_concurrent_genetic_algorithm(population_size, n, patientOne, mutation_rate, generations, num_arrays, shifts_per_day)
print(results)
for i, (best_individual, fitness) in enumerate(results):
    print(f"Best individual {i + 1}: {best_individual}, Fitness: {fitness}")

#best_overall_individual, best_overall_fitness = max(results, key=lambda x: x[1])
#print(f"\n\nBest overall individual: {best_overall_individual}, Fitness: {best_overall_fitness}")