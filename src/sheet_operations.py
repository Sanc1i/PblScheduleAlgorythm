from openpyxl import load_workbook
import re


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
    Fill a cell in an Excel sheet with provided text. If the cell already contains similar content,
    merge the group numbers instead of overwriting.
    
    Args:
        sheet (Worksheet): An openpyxl worksheet object.
        cell_address (str): Cell address (e.g., "A1") to fill.
        text_to_fill (str): Text to fill or merge with existing content.
    """
    cell = sheet[cell_address]
    if cell.value is None:
        cell.value = text_to_fill
    else:
        existing_text = str(cell.value)
        # Extract group numbers from both existing text and new text
        existing_groups = set(re.findall(r'Group (\d+)', existing_text))
        new_groups = set(re.findall(r'Group (\d+)', text_to_fill))
        merged_groups = sorted(existing_groups.union(new_groups), key=int)
        merged_group_text = f"Group {'-'.join(merged_groups)}"
        # Replace the old group part with the merged group text
        updated_text = re.sub(r'Group [\d\-]+', merged_group_text, existing_text)
        cell.value = updated_text
        

# Example usage:
# if not is_cell_occupied("example.xlsx", "Sheet1", "B2"):
#     fill_cell("example.xlsx", "Sheet1", "B2", "Hello World")
