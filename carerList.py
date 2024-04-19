class CarerList:
    def __init__(self, patientName):
        self.carersAvailable = []
        self.patientName = patientName
    
    def add_to_list(self, carer):
        self.carersAvailable.append(carer)
        
    
    def remove_from_list(self, carer):
        self.carersAvailable.remove(carer)
            
    def get_carer_names(self):
        names = []
        for carer in self.carersAvailable:
            #print(carer.name)
            names.append(carer.name)
        return names
    
    def get_carers_available(self):
        return self.carersAvailable
    
    def get_carer(self, carer):
        names = self.get_carer_names();
        
        try:
            index = names.index(carer)
            return self.carersAvailable[index]
        except Exception:
            return None
        
    
        