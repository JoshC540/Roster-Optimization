class CarerList:
    # Sets up the list, which is the patient's carers
    def __init__(self, patientName):
        self.carersAvailable = []
        self.patientName = patientName
    
    # Adds a carer to a list
    def add_to_list(self, carer):
        self.carersAvailable.append(carer)
        
    # Removes a carer to a list
    def remove_from_list(self, carer):
        self.carersAvailable.remove(carer)
           
    # Gets a carers names
    def get_carer_names(self):
        names = []
        
        #Loops through carers and adds the names to a list. This list of carer name is used for making the arrays
        for carer in self.carersAvailable:
            #print(carer.name)
            names.append(carer.name)
        return names
    
    # Returns the list of carers
    def get_carers_available(self):
        return self.carersAvailable
    
    # Get a specfic carer
    def get_carer(self, carer):
        names = self.get_carer_names();
        
        try:
            # Gets the index of the name from the names list
            index = names.index(carer)
            # Returns the carer object at that same index
            return self.carersAvailable[index]
        except Exception:
            return None
    
    # Gets carers who have days = True
    def get_day_carers(self):
        eligible_carers = [carer.name for carer in self.carersAvailable if carer.days]
        return eligible_carers
   
    # Gets carers who have nights = True
    def get_night_carers(self):
        eligible_carers = [carer.name for carer in self.carersAvailable if carer.nights]
        return eligible_carers
        
        
    
        