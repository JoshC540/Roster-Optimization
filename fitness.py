from collections import Counter


def determine_fitness(individual, carerList):
    score = 0
    last_name = ""
    #print(individual)
    for i, group in enumerate(individual):
        #print(group)
        if len(group) != 2:
            score = score - 1000
        else:
            #Ensures names are unique on a day
            if len(group) == len(set(group)): 
                #Patterns
                for j in range(0, len(group)):
                    #print(group)
                    name = group[j]
                    #print(name)
                    carer = carerList.get_carer(name)
                    #print(carer)
                    
                    
                    #if its a day
                    if j == 0:
                        if group[j] == individual[i - 1][j]:
                            if carer.preferredPatternDay == 1:  
                                score = score + 10
                            elif carer.preferredPatternDay == 2:
                                score = score - 5
                        else:
                            if carer.preferredPatternDay == 2:
                                score = score + 10
                            elif carer.preferredPatternDay == 1:
                                score = score - 5
                    if j == 1:
                        if group[j] == individual[i - 1][j]:
                            if carer.preferredPatternNight == 1:      
                                score = score + 10
                            elif carer.preferredPatternNight == 2:
                                score = score - 5
                        else:
                            if carer.preferredPatternNight == 2:
                                score = score + 10
                            elif carer.preferredPatternNight == 1:
                                score = score - 5
                    
                    if carer.days == True and j == 0:      
                        score = score + 50
                    elif carer.nights == True and j == 1:      
                        score = score + 50
                    else:
                        score = score - 10000
                    
                        
                    
                    #Checking between days
                    if last_name == name:
                        score = score - 10000

                    
                    last_name = name
                
                    day_index = (i % 7)
                    carer_days = carer.prefferedDays
        
                    if carer_days[day_index] == 1:
                        score += 50
                    elif carer_days[day_index] == -1:
                        score -= 10
                        
            else:
                score = score - 10000



    flattened_list = [item for sublist in individual for item in sublist]

    shift_count = Counter(flattened_list)

    for carer, count in shift_count.items():
        if count / 6 > 5:
            score = score - 10000
        if count / 6 > 4:
            score = score - 1000
        if count / 6 < 2:
            score = score - 100
        if count / 6 <= 4:
            score = score + 10

    
  
    if score < 0:
        score = 1
        
    return score


"""
OLD

    for i in range(1, len(individual)):
        name = individual[i]
        carer = carerList.get_carer(name)
        
        if individual[i] == individual[i-1] and carer.preferredPatternDay == 1:      
            score = score + 4
        elif individual[i] == individual[i-1] and carer.preferredPatternDay == 2:
            score = score - 5
        
        elif individual[i] != individual[i-1] and carer.preferredPatternDay == 2:
            score = score + 4
        elif individual[i] != individual[i-1] and carer.preferredPatternDay == 1:
            score = score - 5
        
        day_index = 7 - (32 % 7) -1
        carer_days = carer.prefferedDays
        
        if carer_days[day_index] == 1:
            score = score + 20
        elif carer_days[day_index] == -1:
            score = score - 25
    
    element_count = Counter(individual)

    # Print the count of each element
    for name, count in element_count.items():
        
        carer = carerList.get_carer(name)
        carer.numberOfShifts = count
        
        average_weekly_hours = (count * 12) / (len(individual) // 7)
        carer.averageHours = average_weekly_hours
        
        if count > 4 * (len(individual) / 7):
            score = score - 2000
        if count < (len(individual) / 6) - 3:
            score = score - 2000
        #if average_weekly_hours > 41:
        #    score = score - 2000
        #if average_weekly_hours > 60:
        #    score = score - 50000
  """

    
        
    