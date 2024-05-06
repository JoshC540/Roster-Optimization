from collections import Counter
from datetime import datetime, timedelta


"""
    This file is tasked with the calculation of fitness, this is used to determine the best scoring individuals of a generation
"""



# Placeholder date time
start_date = "2024-0-1"

# Takes a date time and sets to be the start date
# This is used later to check for days off
def set_start_date(new_start_date):
    global start_date
    start_date = new_start_date
    #print(start_date)




def determine_fitness(individual, carerList):
    # Score is the fitness, higher is better
    score = 0
    # Last name is used to track someone isnt working consectutive shifts
    last_name = ""
    # Num weeks is used to check average shifts a week
    num_weeks = (len(individual) // 7)
    
    for i, group in enumerate(individual):
        #Group is the shifts of a set day, in the format ["name 1", "name 2"]
        #print(group)
        
        # If there is not a day and night shift it is a fail so we dont do more code
        if len(group) != 2:
            score = score - 1000
        else:
            #Ensures names are unique on a day
            if len(group) == len(set(group)): 
                for j in range(0, len(group)):
                    #print(group)
                    name = group[j]
                    #print(name)
                    carer = carerList.get_carer(name)
                    #print(carer)
                    
                    #Checks if carer can work a certain day
                    if len(carer.daysOff) > 0:
                        unavailable_dates = carer.daysOff
                        current_date = start_date + timedelta(days=i)          
                        # Check if the current date is not in the list of unavailable dates
                        if current_date.strftime("%Y-%m-%d") in unavailable_dates and (group[0] == carer.name or group[1] == carer.name):
                            #print(f"{name}, cannot work {current_date}")
                            return 1
                    
                    # Checking patterns such as every second day or shifts in a row
                    # 0 = N/A, 1 = consecutive, 2 = every second day
                    
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
                    # If night
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
                    
                    # Rewarding if the carer can work the day or night
                    if carer.days == True and j == 0:      
                        score = score + 50
                    elif carer.nights == True and j == 1:      
                        score = score + 50
                    else:
                        # Fail if someone is set to a day or night shift if they can not work them
                        score = score - 10000
                    
                    #Checking between days
                    if last_name == name:
                        score = score - 10000  
                    last_name = name
                
                    # Getting which day of the week it is
                    day_index = (i % 7)
                    # if day 
                    if j == 0:
                        carer_days = carer.prefferedDays
                        #If they prefer working this day, reward
                        if carer_days[day_index] == 1:
                            score += 50
                        # If they prefer not to, reduce score
                        elif carer_days[day_index] == -1:
                            score -= 10
                    # if night
                    if j == 1:
                        carer_night = carer.prefferedNights
                        
                        # Same logic as days but for nights
                        if carer_night[day_index] == 1:
                            score += 50
                        elif carer_night[day_index] == -1:
                            score -= 10
                            
                    
                        
            else:
                # If name arent unique on a day, the roster is illegal
                score = score - 10000

    
    # Makes array 1d so we can count the occurances
    flattened_list = [item for sublist in individual for item in sublist]
    
    # Counts occurance of each name
    shift_count = Counter(flattened_list)

    # Increase and decrease score based on count
    for carer, count in shift_count.items():
        if count / num_weeks > 5:
            score = score - 10000
        if count / num_weeks > 4:
            score = score - 1000
        if count / num_weeks < 2:
            score = score - 100
        if count / num_weeks <= 4:
            score = score + 10

    
    

    # Weights are used so negative scores casue issus so if it is negative we set it to 1 and this is the only way 1 can be scored
    if score < 0:
        score = 1
        
    return score

