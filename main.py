from carer import Carer
from carerList import CarerList
from GA import run_concurrent_genetic_algorithm
from RM import run_reward_machine
from scheduler import create_schedule
import time
from datetime import datetime
import json
import graphing
from fitness import set_start_date
from rosterTool import roster_tool


# Loads in a carer list from a json file. Used for storing carer lists in a readable way
# Future work would use a database
def load_carers_from_json(filename, patient):
    with open(filename, 'r') as file:
        data = json.load(file)
    for carer_data in data['carers']:
        carer = Carer(
            carer_data['name'],
            carer_data['preferredPatternDay'],
            carer_data['preferredPatternNight'],
            carer_data['preferredDays'],
            carer_data['preferredNights'],
            carer_data['daysOff'],
            carer_data['days'],
            carer_data['nights']
        )
        patient.add_to_list(carer)
        
# Runs a hard coded roster with the paraters easy to change for testing.
def demo_Roster():
    
    # Record the start time
    start_time = time.time()
    
    # List of hard coded variables, in the tool itself most of these can be set by the user
    patientOne = CarerList("John")
    load_carers_from_json('carers.json', patientOne)
    
    
    start_date = datetime(2024, 4, 29)
    set_start_date(start_date)
    
    num_of_weeks = 6
    n = 7 * num_of_weeks  # Length of the array
    mutation_rate = 0.01
    
    #===================
    # These values are lower than I found advisable but they make sure it runs quickly
    generations = 50
    population_size = 100
    #=====================
    shifts_per_day = 1
    shifts_per_night = 1
    num_arrays = 1  # Number of arrays to generate concurrently
    
    
    
    results = run_concurrent_genetic_algorithm(population_size, n, patientOne, mutation_rate, generations, num_arrays, shifts_per_day, shifts_per_night)
    print(results)
    for i, (best_individual, fitness) in enumerate(results):
        print(f"Best individual {i + 1}: {best_individual}, Fitness: {fitness}")
    
    best_overall_individual, best_overall_fitness = max(results, key=lambda x: x[1])
    print(f"\n\nBest overall individual: {best_overall_individual}, Fitness: {best_overall_fitness}")
    
    
    
    if best_overall_fitness == 1:
        print("The was no legal or suitable roster able to be found")
    else:
        create_schedule("weekly_schedule.xlsx", start_date, num_of_weeks, data = best_overall_individual)
    
    
    # Record the end time
    end_time = time.time()
    
    # Print the start and end times
    print("")
    print("")
    print("")
    print("")
    print("Start Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    print("End Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
    
    # Calculate and print the total execution time
    execution_time = end_time - start_time
    print("Total Execution Time:", execution_time, "seconds")


def main():
    
    #========================================================
    # Using the sample patient for all graphs for consistancy
    patientGraph = CarerList("John")

    # Load carers from JSON and add them to patientOne
    load_carers_from_json('carers.json', patientGraph)
    #========================================================

    # Simple text menu
    while True:
        print("="*25)
        print("Roster Generation System:")
        print("="*25)
        print("1. Graph  genetic algorithm and display fitness vs generations graph")
        print("2. Graph  genetic algorithm and display fitness vs populations graph")
        print("3. Graph genetic algorithm and display fitness vs mutation rates")
        print("4. Run reward machine - Not Functional")
        print("5. Make Roster (DEMO) ")
        print("6. Make Roster (TOOL) ")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            start_date = datetime(2024, 4, 29)
            set_start_date(start_date)
            graphing.plot_generations_vs_fitness(100, 42, patientGraph, 0.01, 1, 1)
            
        elif choice == "2":
            start_date = datetime(2024, 4, 29)
            set_start_date(start_date)
            graphing.plot_populations_vs_fitness(1000, 42, patientGraph, 0.01, 1, 1)
            
        elif choice == "3":
            start_date = datetime(2024, 4, 29)
            set_start_date(start_date)
            graphing.plot_mutation_rates_vs_fitness(1000, 1000, 1, patientGraph, 1, 1)
        
        # Reward Machine - Broken
        # I was unable to make this generate results that work but the code is here anywats
        elif choice == "4":
            
            patientOne = CarerList("John")
            load_carers_from_json('carers.json', patientOne)
            
            
            num_of_weeks = 6
            population_size = 100
            n = 7 * num_of_weeks  # Length of the array
            mutation_rate = 0.01
            generations = 50
            shifts_per_day = 1
            shifts_per_night = 1

            
            results, best = run_reward_machine(population_size, mutation_rate, n, patientOne, generations, shifts_per_day, shifts_per_night)
            print(results)
            print(best)
            
        elif choice == "5":
            # Fast roster
            demo_Roster()
            
        elif choice == "6":
            # Actual tool
            roster_tool()
            
            break
        elif choice == "7":
            print("Exiting...")
            
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()


