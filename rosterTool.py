from carer import Carer
from carerList import CarerList
from GA import run_concurrent_genetic_algorithm
from scheduler import create_schedule
import time
from datetime import datetime
import json
from fitness import set_start_date
from patientManagement import get_patients, add_patient, remove_patient


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
        
#==============================================================================
# Super basic input validation, more is needed to ensure all data is correct
# But this at least helps reduce bad input

# Basic boolean input validation
def get_bool_input(prompt):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower()]
        except KeyError:
            print("Please enter 'true' or 'false'.")

# Ensuring we have an int when expected
def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")
#==============================================================================

# Handles adding carers for a patient
def add_carers(total_count):
    carers = []
    count = 0
    while count < total_count:
        count = count + 1
        name = input(f"Enter carer's name ({count}/{total_count}): ")
        if name.lower() == 'done':
            break

        preferred_pattern_day = get_int_input("0 = N/A\n1 = consecutive\n2 = every second day \nEnter preferred pattern for day shift: ")
        preferred_pattern_night = get_int_input("0 = N/A\n1 = consecutive\n2 = every second day \nEnter preferred pattern for night shift: ")
        print("0 = N/A\n1 = prefers\n-1 = prefer not")
        preferred_days = [get_int_input(f"Enter preference for day {i + 1}: ") for i in range(7)]
        print("0 = N/A\n1 = prefers\n-1 = prefer not")
        preferred_nights = [get_int_input(f"Enter preference for night {i + 1}: ") for i in range(7)]
        days_off_input = input("Enter days off (comma-separated in format of YYYY-MM-DD, or leave empty if none): ")
        days_off = [] if days_off_input.strip() == '' else days_off_input.split(',')
        days = get_bool_input("Does this carer work days? (true/false): ")
        nights = get_bool_input("Does this carer work nights? (true/false): ")

        carer = {
            "name": name,
            "preferredPatternDay": preferred_pattern_day,
            "preferredPatternNight": preferred_pattern_night,
            "preferredDays": preferred_days,
            "preferredNights": preferred_nights,
            "daysOff": days_off,
            "days": days,
            "nights": nights
        }
        
        if total_count == 1:
            return carer
        
        carers.append(carer)

    carer_data = {"carers": carers}
    
    return carer_data

# Adds a single carer from a json
def add_carer(existing_carers, carer):
    existing_carers["carers"].append(carer)
  
    
# Deletes a single carer from a json
def delete_carer(json_data, name):
    for carer in json_data["carers"]:
        if carer["name"] == name:
            json_data["carers"].remove(carer)
            return True  # Return True if deletion is successful
    return False  # Return False if carer with specified name is not found


# Simple menu. With more time this would be a GUI
def roster_tool():
    while True:
        print("\n"*2)
        print("="*25)
        print("Rostering Tool:")
        print("="*25)
        print("1. View Patients")
        print("2. Add Patient")
        print("3. Remove Patient")
        print("4. View Patient Details")
        print("5. Add Carers")
        print("6. Remove Carer")
        print("7. Make Roster")
        print("8. Exit")
    
        choice = input("Enter your choice: ")
        
        # Viewing patient files
        if choice == "1":
            patients = get_patients()
    
            # JSON file paths
            print("Patients files:")
            for patient in patients:
                print(patient)
         
        # Adding patient file
        elif choice == "2":
           patient_to_add = input("Enter patient to add: ")
           
           #Gets number of carers
           number_of_carers = get_int_input("How many carers?")
           # Makes that many carers with user input
           carer_data = add_carers(number_of_carers)
           
           file_name = patient_to_add.lower().replace(" ", "_") + ".json"
           
           add_patient(carer_data, file_name)
           
        # Deleting patient file
        elif choice == "3":
            patients = get_patients()
    
            # JSON file paths
            print("Patients files:")
            for patient in patients:
                print(patient)
                
            patient_to_remove = input("Enter patient name to delete: ")
            patient_to_remove = patient_to_remove.lower() + ".json"
            
            remove_patient(patient_to_remove)
        
        # Viewing Patient Details, just printing the json
        elif choice == "4":
            patients = get_patients()
    
            # JSON file paths
            print("Patients files:")
            for patient in patients:
                print(patient)
            
            patient_to_view = input("Enter patient name to view: ")
            patient_to_view = f"patients/{patient_to_view.lower()}.json"
            print(patient_to_view)
            
            try:
               # Open the JSON file
               with open(patient_to_view, 'r') as file:
                   # Load JSON data
                   patient_data = json.load(file)
                   # Print in readable form
                   print(json.dumps(patient_data, indent=4))
            except FileNotFoundError:
               print("File not found.")
       
        # Add carers to patient
        elif choice == "5":
            patients = get_patients()
    
            #JSON file paths
            print("Patients files:")
            for patient in patients:
                print(patient)
            
            patient_to_view = input("Enter patient name to add carer to: ")
            patient_to_view = f"patients/{patient_to_view.lower()}.json"
            
            # Make 1 carer
            carer = add_carers(1)
            
            try:
               # Open the JSON file
               with open(patient_to_view, 'r') as file:
                   existing_carers = json.load(file)
            except FileNotFoundError:
               print("File not found.")
             
            add_carer(existing_carers, carer)
            with open(patient_to_view, 'r') as file:
                existing_carers = json.load(file)
          
        # Remove carer 
        elif choice == "6":
            patients = get_patients()
    
            # JSON file paths
            print("Patients files:")
            for patient in patients:
                print(patient)
            
            patient_to_view = input("Enter patient name to remove carer from: ")
            patient_to_view = f"patients/{patient_to_view.lower()}.json"
            
            
            try:
               # Open the JSON file
               with open(patient_to_view, 'r') as file:
                   existing_carers = json.load(file)
            except FileNotFoundError:
               print("File not found.")
             
            carer_to_remove = input("Enter carer name to remove: ")
            
            deleted = delete_carer(existing_carers, carer_to_remove)

            if deleted:
                print(f"Carer '{carer_to_remove}' deleted successfully.")
            else:
                print(f"Carer '{carer_to_remove}' not found.")
            
            with open(patient_to_view, 'r') as file:
                existing_carers = json.load(file)
        
        # Make a roster
        elif choice == "7":
            # Record the start time
            start_time = time.time()
            
            patientName = input("What is the patients name?")
            
            patient = CarerList(patientName)
            
            
            invalid_file = True
            while invalid_file:
                patient_file_name = input("What is the patients file name?")
                patient_json = f"patients/{patient_file_name}.json"
                try:
                   # Open the JSON file
                   with open(patient_json, 'r') as file:
                       load_carers_from_json(patient_json, patient)
                       invalid_file = False
                except FileNotFoundError:
                   print("File not found.")
            
            
            while True:
                user_input = input("Enter the start date (Format: YYYY-MM-DD, Date assumed to be Sunday): ")
                
                try:
                    start_date = datetime.strptime(user_input, "%Y-%m-%d")
                    set_start_date(start_date)
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            
            
            num_of_weeks = get_int_input("How many weeks do you want to roster: ")

            n = 7 * num_of_weeks  # Length of the array
            
            population_size = 1000
            mutation_rate = 0.01
            generations = 1000
            
            # Currently only support 1 per - future work adding more
            shifts_per_day = 1
            shifts_per_night = 1
            
            num_arrays = 10  # Number of rosters to generate concurrently
            

            
            
            
            results = run_concurrent_genetic_algorithm(population_size, n, patient, mutation_rate, generations, num_arrays, shifts_per_day, shifts_per_night)
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
            
        elif choice == "8":
            print("Exiting...")
            
            break
        else:
            print("Invalid choice. Please enter a valid option.")