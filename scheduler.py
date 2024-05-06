from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from datetime import timedelta

# Makes an excel for the scheudle 
def create_schedule(filename, start_date, weeks=6, data=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly Schedule"

    # Days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Inserting days of the week
    ws.append([""] + days)
    
    # Weekly Arrays
    weeks_array = []
    
    for i in range(0, len(data), 7):
        # Slice the original array to get 7 arrays of 2 elements
        seven_arrays = data[i:i+7]
        
        # Append these 7 arrays to the result array
        weeks_array.append(seven_arrays)

    # Inserting day and night shift headers on the left edge for each date
    current_date = start_date
    for i in range(weeks):
        current_week_names = weeks_array[i]
        dates = []
        for _ in range(7):
            dates.append([current_date.strftime("%d-%m-%Y")])
            current_date += timedelta(days=1)
        ws.append(["Dates:"] + dates[0] + dates[1] + dates[2] + dates[3] + dates[4] + dates[5] + dates[6])
        ws.append(["Day Shift:"] + [current_week_names[0][0]] + [current_week_names[1][0]] + [current_week_names[2][0]] + [current_week_names[3][0]] +[ current_week_names[4][0]] + [current_week_names[5][0]] + [current_week_names[6][0]])
        ws.append(["Night Shift:"] + [current_week_names[0][1]] + [current_week_names[1][1]] + [current_week_names[2][1]] + [current_week_names[3][1]] + [current_week_names[4][1]] + [current_week_names[5][1]] + [current_week_names[6][1]])
    
    # Formatting cells
    for row in ws.iter_rows(min_row=1, max_row=100, min_col=2):
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.font = Font(color="000000")  # Black font color
    
    # Save the workbook
    wb.save(filename)
