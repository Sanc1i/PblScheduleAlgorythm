from openpyxl import load_workbook

def is_cell_occupied(sheet, cell_address):
    """
    Check if a cell in an Excel sheet contains data.
    
    Args:
        sheet (Worksheet): An openpyxl worksheet object.
        cell_address (str): Cell address (e.g., "A1") to check.
    
    Returns:
        bool: True if the cell is occupied, False if it's empty.
    """
    cell = sheet[cell_address]
    return cell.value is not None 

def fill_cell(sheet, cell_address, text_to_fill):
    """
    Fill a cell in an Excel sheet with provided text if it is empty.
    
    Args:
        sheet (Worksheet): An openpyxl worksheet object.
        cell_address (str): Cell address (e.g., "A1") to fill.
        text_to_fill (str): Text to fill if the cell is empty.
    """
    cell = sheet[cell_address]
    if cell.value is None:
        cell.value = text_to_fill
        print(f"Cell {cell_address} was empty. Filled with: '{text_to_fill}'")
    else:
        print(f"Cell {cell_address} already contains data: '{cell.value}'")

# Example usage:
# if not is_cell_occupied("example.xlsx", "Sheet1", "B2"):
#     fill_cell("example.xlsx", "Sheet1", "B2", "Hello World")
