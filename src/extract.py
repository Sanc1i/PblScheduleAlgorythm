import numpy as np

def extract_names(data):
    """
    Extracts the names of tutors from the given list and returns them as an array.
    
    Parameters:
        data (list): A list of tuples where each tuple contains tutor details.
        
    Returns:
        numpy.ndarray: An array of tutor names.
    """
    # Extract names (First Name + Last Name) from the data
    names = [f"{record[1]}_{record[2]}" for record in data]
    
    # Convert to a NumPy array
    return np.array(names)

def extract_data(data):
    """
    Extracts the names of tutors from the given list and returns them as an array.
    
    Parameters:
        data (list): A list of tuples where each tuple contains tutor details.
        
    Returns:
        numpy.ndarray: An array of tutor names.
    """
    # Extract names (First Name + Last Name) from the data
    names = [f"{record[1]}" for record in data]
    
    # Convert to a NumPy array
    return np.array(names)

# def extract_faculties(data):
#     """
#     Extracts the names of tutors from the given list and returns them as an array.
    
#     Parameters:
#         data (list): A list of tuples where each tuple contains tutor details.
        
#     Returns:
#         numpy.ndarray: An array of tutor names.
#     """
#     # Extract names (First Name + Last Name) from the data
#     names = [f"{record[0]}" for record in data]
    
#     # Convert to a NumPy array
#     return np.array(names)

def extract_group(data):
    """
    Extracts the names of tutors from the given list and returns them as an array.
    
    Parameters:
        data (list): A list of tuples where each tuple contains tutor details.
        
    Returns:
        numpy.ndarray: An array of tutor names.
    """
    # Extract names (First Name + Last Name) from the data
    
    names = [f"Faculty{record[1]}_Group{record[2]}" for record in data]
    
    # Convert to a NumPy array
    return np.array(names)

def extract_all(groups, rooms, tutors):
    # names = np.concatenate((extract_names(groups), extract_data(rooms), extract_names(tutors)))
    names = np.concatenate((extract_group(groups), extract_data(rooms), extract_names(tutors)))
    return names