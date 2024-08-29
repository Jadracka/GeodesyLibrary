import numpy as np
import os
from collections import defaultdict

def read_point_file(file_path):
    """
    Reads point data from a text file and returns a dictionary of points.
    
    Args:
        file_path (str): Path to the text file containing point data.
        
    Returns:
        dict: A dictionary where the keys are point IDs (PoID) and the values 
              are dictionaries containing coordinates, sigmas, sigma_mag, and 
              covariance matrix for each point.
    """
    points = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            PoID = parts[0]
            coords = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
            sigmas = np.array([float(parts[4]), float(parts[5]), float(parts[6])])
            sigma_mag = float(parts[7])
            cov_matrix = np.array([
                [float(parts[8]), float(parts[9]), float(parts[10])],
                [float(parts[11]), float(parts[12]), float(parts[13])],
                [float(parts[14]), float(parts[15]), float(parts[16])]
            ])
            points[PoID] = {
                'coords': coords,
                'sigmas': sigmas,
                'sigma_mag': sigma_mag,
                'cov_matrix': cov_matrix
            }
    return points

def aggregate_points(file_paths):
    """
    Aggregates points from multiple files into a single dictionary.
    
    Args:
        file_paths (list): List of file paths containing point data.
        
    Returns:
        dict: A dictionary where the keys are point IDs (PoID) and the values 
              are lists of point data dictionaries from each file.
    """
    all_points = defaultdict(lambda: {'instances': [], 'sources': []})
    for file_path in file_paths:
        points = read_point_file(file_path)
        for PoID, data in points.items():
            all_points[PoID]['instances'].append(data)
            all_points[PoID]['sources'].append(os.path.basename(file_path))
    return all_points

def combine_points(all_points):
    """
    Combines instances of each point using the weighted averaging algorithm 
    and calculates new coordinates and covariance matrices.
    
    Args:
        all_points (dict): A dictionary where the keys are point IDs (PoID) and 
                           the values are dictionaries with instances of point 
                           data and the sources they came from.
    
    Returns:
        dict: A dictionary where the keys are point IDs (PoID) and the values 
              are dictionaries containing the new coordinates, combined covariance 
              matrix, standard deviations, number of instances, and sources of each point.
    """
    combined_points = {}
    for PoID, data in all_points.items():
        instances = data['instances']
        points = [instance['coords'] for instance in instances]
        cov_matrices = [instance['cov_matrix'] for instance in instances]
        
        # Calculate inverse covariance matrices
        inv_cov_matrices = [np.linalg.inv(cov) for cov in cov_matrices]
        
        # Calculate the combined covariance matrix
        combined_cov_matrix = np.linalg.inv(sum(inv_cov_matrices))
        
        # Calculate the weighted sum of points
        weighted_sum_points = sum(W @ p for W, p in zip(inv_cov_matrices, points))
        
        # Calculate the averaged point
        avg_point = combined_cov_matrix @ weighted_sum_points
        
        # Calculate standard deviations from the combined covariance matrix
        sigma_x = np.sqrt(combined_cov_matrix[0, 0])
        sigma_y = np.sqrt(combined_cov_matrix[1, 1])
        sigma_z = np.sqrt(combined_cov_matrix[2, 2])
        
        # Calculate standard deviation of the magnitude
        sigma_mag = np.sqrt(np.trace(combined_cov_matrix))
        
        # Calculate combined sigma_xy
        sigma_xy = np.sqrt(sigma_x**2 + sigma_y**2)
        
        combined_points[PoID] = {
            'coords': avg_point,
            'cov_matrix': combined_cov_matrix,
            'sigma_x': sigma_x,
            'sigma_y': sigma_y,
            'sigma_z': sigma_z,
            'sigma_mag': sigma_mag,
            'sigma_xy': sigma_xy,
            'num_instances': len(instances),
            'sources': list(set(data['sources']))  # Only include unique sources
        }
    return combined_points

def print_sorted_points(combined_points):
    """
    Prints the points sorted by their combined sigma_xy.
    
    Args:
        combined_points (dict): A dictionary where the keys are point IDs (PoID) and 
                                the values are dictionaries containing point data.
    """
    sorted_points = sorted(combined_points.items(), key=lambda item: item[1]['sigma_xy'])
    
    for PoID, data in sorted_points:
        print(f"PoID: {PoID}")
        print(f"  Averaged Point Coordinates [mm]: {data['coords']}")
        #print(f"  Combined Covariance Matrix: \n{data['cov_matrix']}")
        #print(f"  Sigma_X: {data['sigma_x']}, Sigma_Y: {data['sigma_y']}, Sigma_Z: {data['sigma_z']}, Sigma_mag: {data['sigma_mag']}, Sigma_XY: {data['sigma_xy']}")
        print(f"  Sigma_XY: {data['sigma_xy']:.4f} mm")
        print(f"  Number of Instances: {data['num_instances']}")
        #print(f"  Sources: {data['sources']}")
        print()


def write_combined_points_to_file(combined_points, output_file_path):
    """
    Writes the combined points to a text file in the specified format:
    PointID X Y Z SigmaX SigmaY SigmaZ
    
    Args:
        combined_points (dict): Dictionary where keys are point IDs (PoID) and
                                values are dictionaries containing point data.
        output_file_path (str): Path to the output text file.
    
    Raises:
        IOError: If the file cannot be created or written to.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        with open(output_file_path, 'w') as file:
            # Write header with comment characters
            file.write('# Point data file\n')
            file.write('# Format: PointID X Y Z SigmaX SigmaY SigmaZ\n')
            
            for PoID, data in combined_points.items():
                line = (
                    f"{PoID} "
                    f"{data['coords'][0]:.6f} {data['coords'][1]:.6f} {data['coords'][2]:.6f} "
                    f"{data['sigma_x']:.6f} {data['sigma_y']:.6f} {data['sigma_z']:.6f}\n"
                )
                file.write(line)
    except Exception as e:
        raise IOError(f"Error writing to file {output_file_path}: {e}")

# Define the paths to the text files
file_paths = ['Helpers/0_Point List.txt', 'Helpers/1_Point List.txt', 'Helpers/2_Point List.txt']

# Read and aggregate points from the text files
all_points = aggregate_points(file_paths)

# Combine points and calculate the new coordinates, covariance matrices, and standard deviations
combined_points = combine_points(all_points)

# Print the sorted points by their sigma_xy
print_sorted_points(combined_points)

output_file_path = 'Helpers/output.txt'
write_combined_points_to_file(combined_points, output_file_path)