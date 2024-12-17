import os
from openpyxl import Workbook

FOLDER_NAME = "schedules"

current_folder = os.path.dirname(__file__)  # Folder where the script is located
schedule_folder = os.path.join(current_folder, "..", FOLDER_NAME)  # Go one level up and into "schedule"

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
class_times = ["8:15 - 10:00", "10:15 - 12:00", "12:15 - 14:00", "14:15 - 16:00", "16:15 - 18:00", "18:15 - 20:00"]

def createFile(name = str, amount_of_sheets = int):
    if not os.path.exists(schedule_folder):
        os.makedirs(schedule_folder)
    wb = Workbook()

    default_sheet = wb.active
    default_sheet.title = "Schedule_1"

    createSchedule(default_sheet)

    num_sheets = amount_of_sheets
    for i in range(2, num_sheets + 1):
        sheet_name = f"Schedule_{i}"
        new_sheet = wb.create_sheet(title=sheet_name)
        createSchedule(new_sheet)

    # Save the workbook in the "schedule" folder
    file_path = os.path.join(schedule_folder, name + ".xlsx")
    wb.save(file_path)

    print(f"Excel file has been saved at: {file_path}")


def createSchedule(sheet):
        for col, day in enumerate(days, start=2):
            sheet.cell(row=1, column=col, value=day)

        for row, time in enumerate(class_times, start=2):
            sheet.cell(row=row, column=1, value=time)