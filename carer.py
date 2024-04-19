class Carer:
    def __init__(self, name, preferredPatternDay, preferredPatternNight, preferredDays, preferredNights, numberOfShifts, averageHours, daysOff, days, nights):
        self.name = name
        self.preferredPatternDay = preferredPatternDay
        self.preferredPatternNight = preferredPatternNight
        self.prefferedDays = preferredDays
        self.prefferedNights = preferredNights
        self.numberOfShifts = numberOfShifts
        self.averageHours = averageHours
        self.daysOff = daysOff
        self.days = days
        self.nights = nights
        
# Name is name
# preferredPatternDay: 0 = N/A, 1 = consecutive, 2 = every second day
# preferredPatternNight: 0 = N/A, 1 = consecutive, 2 = every second night 
# prefferedDays is an array of seven, 1 is want, 0 is neutral and -1 is not want
# prefferedNights see preferred days
# averageHours over 6 weeks needs to be aroud 40
# daysOff list of dates they are unavailbe for
# days, True or False if they can work them
# nights, True or False if they can work them

