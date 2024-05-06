import os
import json


"""
    This handles creation of, deleting of and viewing of the various JSON files. Currently it is one per patient
    The JSON contains all of their carer information
"""
# Folder where patient JSON are, can be changed here to store them elsewhere
patient_folder_path = "patients"

# Gets a list of JSON and returns them
def get_patients():
    patient_files = []
    # Iterate through all files in the folder
    for file_name in os.listdir(patient_folder_path):
        # Check if JSON 
        if file_name.endswith('.json'):
            file_path = os.path.join(patient_folder_path, file_name)
            patient_files.append(file_path)
    
    return patient_files

# Makes a new patient file with all of its carer information
def add_patient(json_data, file_name):
    file_path = os.path.join(patient_folder_path, file_name)
    with open(file_path, 'w') as f:
        json.dump(json_data, f)

# Deletes a JSON if it exists
def remove_patient(file_name):
    try:
        file_path = os.path.join(patient_folder_path, file_name)
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File '{file_name}' not found in folder '{patient_folder_path}'.")
