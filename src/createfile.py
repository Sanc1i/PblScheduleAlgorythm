import os
from openpyxl import Workbook

# Define the relative path to the "schedule" folder
current_folder = os.path.dirname(__file__)  # Folder where the script is located
schedule_folder = os.path.join(current_folder, "..", "schedules")  # Go one level up and into "schedule"

# Create the folder if it doesn't exist
if not os.path.exists(schedule_folder):
    os.makedirs(schedule_folder)

# Create a new workbook
wb = Workbook()

# Rename the default sheet (if needed)
default_sheet = wb.active
default_sheet.title = "Schedule_1"

# Define days of the week and class times
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
class_times = [
    "8:15 - 10:00",
    "10:15 - 12:00",
    "12:15 - 14:00",
    "14:15 - 16:00",
    "16:15 - 18:00",
    "18:15 - 20:00"
]

# Function to populate each sheet
def populate_sheet(sheet):
    # Write days in the first row
    for col, day in enumerate(days, start=2):  # Start at column 2 (B)
        sheet.cell(row=1, column=col, value=day)

    # Write class times in the first column
    for row, time in enumerate(class_times, start=2):  # Start at row 2
        sheet.cell(row=row, column=1, value=time)

# Populate the default sheet
populate_sheet(default_sheet)

# Create additional sheets and populate them
num_sheets = 10  # You can change this to the number of sheets you need
for i in range(2, num_sheets + 1):
    sheet_name = f"Schedule_{i}"
    new_sheet = wb.create_sheet(title=sheet_name)
    populate_sheet(new_sheet)

# Save the workbook in the "schedule" folder
file_path = os.path.join(schedule_folder, "Schedules.xlsx")
wb.save(file_path)

print(f"Excel file has been saved at: {file_path}")
