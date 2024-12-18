import numpy as np

def extract_tutor_names(data):
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

def extract_rest(data):
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