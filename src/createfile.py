import os
from openpyxl import Workbook
import constants


def createFile(name = str, amount_of_sheets = int):
    current_folder = os.path.dirname(__file__)
    schedule_folder = os.path.join(current_folder, "..", constants.FOLDER_NAME)
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

    file_path = os.path.join(schedule_folder, name + ".xlsx")
    wb.save(file_path)

    print(f"Excel file has been saved at: {file_path}")


def createSchedule(sheet):
        for col, day in enumerate(constants.DAYS, start=2):
            sheet.cell(row=1, column=col, value=day)

        for row, time in enumerate(constants.CLASS_TIMES, start=2):
            sheet.cell(row=row, column=1, value=time)