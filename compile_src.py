import os

def list_files_in_folder(folder_path, output_file):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f != output_file]
        
        imports = []
        all_entries = []
        for file_name in files:
            module_name = os.path.splitext(file_name)[0]
            imports.append(f"from .{module_name} import *")
            all_entries.append(f'"{module_name}"')
        
        output_path = os.path.join(folder_path, output_file)
        with open(output_path, 'w') as f:
            for line in imports:
                f.write(line + '\n')
            f.write('\n')
            f.write(f"__all__ = [{', '.join(all_entries)}]\n")
        
        print(f"File names successfully written to {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

current_folder = os.path.dirname(__file__)
folder_path = os.path.join(current_folder, "src")
output_file = "__init__.py"

list_files_in_folder(folder_path, output_file)
