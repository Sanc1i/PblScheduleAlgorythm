import os
import pandas as pd

def get_sheet_data_as_tuples(sheet_name):

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '..', "DataBase.xlsx")
        
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        
        rows_as_tuples = [tuple(row) for row in data.itertuples(index=False)]
        
        return rows_as_tuples
    except Exception as e:
        print(f"Error processing the sheet '{sheet_name}': {e}")
        return []

def get_sheet_names():

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '..', "DataBase.xlsx")
        
        excel_file = pd.ExcelFile(file_path)
        
        return excel_file.sheet_names
    except Exception as e:
        print(f"Error retrieving sheet names: {e}")
        return []

# sheet_names = get_sheet_names()
# print("Sheet names:", sheet_names)
# sheetdata = get_sheet_data_as_tuples("Groups")
# print(sheetdata)