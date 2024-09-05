import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse

def read_input_file(file_path):
    # Read the text file into a pandas DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Rename columns based on the provided format
    df.columns = [
        'PointID', 'X_m', 'Y_m', 'Z_m', 's_x_mm', 's_y_mm', 's_z_mm',
        'a_mm', 'b_mm', 'c_mm', 'w_a_gon', 'w_b_gon', 'w_c_gon',
        'z_a_gon', 'z_b_gon', 'z_c_gon'
    ]
    return df

# Example usage
file_path = 'V:\Projekte\PETRA4\Simulationen\Girder alignment\PP Outcome\Points_out.txt'
data = read_input_file(file_path)

def plot_error_ellipses(data):
    """
    Plot 2D error ellipses for each point in the data.
    """
    fig, ax = plt.subplots()

    for idx, row in data.iterrows():
        # Extract values
        x, y, s_x, s_y, a, b, w_a, z_a = row['X_m'], row['Y_m'], row['s_x_mm'], row['s_y_mm'], row['a_mm'], row['b_mm'], row['w_a_gon'], row['z_a_gon']
        
        # Convert gon to degrees (1 gon = 0.9 degrees)
        angle = w_a * 0.9

        # Plot ellipse
        ell = Ellipse((x, y), width=2*a, height=2*b, angle=angle, edgecolor='red', facecolor='none')
        ax.add_patch(ell)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.grid(True)
    plt.title('2D Error Ellipses')
    plt.show()

def plot_error_ellipsoids(data):
    """
    Plot 3D error ellipsoids for each point in the data.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for idx, row in data.iterrows():
        # Extract values
        x, y, z, a, b, c, w_a, w_b, w_c = row['X_m'], row['Y_m'], row['Z_m'], row['a_mm'], row['b_mm'], row['c_mm'], row['w_a_gon'], row['w_b_gon'], row['w_c_gon']
        
        # Convert gon to radians (1 gon = 0.9 degrees)
        w_a_rad, w_b_rad, w_c_rad = np.radians([w_a * 0.9, w_b * 0.9, w_c * 0.9])

        # Create a 3D ellipsoid using parametric equations
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        ellipsoid_x = a * np.outer(np.cos(u), np.sin(v))
        ellipsoid_y = b * np.outer(np.sin(u), np.sin(v))
        ellipsoid_z = c * np.outer(np.ones_like(u), np.cos(v))

        # Rotate data to align with the eigenvectors
        ellipsoid_points = np.column_stack((ellipsoid_x.ravel(), ellipsoid_y.ravel(), ellipsoid_z.ravel()))

        # Apply rotations for each axis
        rotation_matrix_a = np.array([[np.cos(w_a_rad), -np.sin(w_a_rad), 0], [np.sin(w_a_rad), np.cos(w_a_rad), 0], [0, 0, 1]])
        rotation_matrix_b = np.array([[np.cos(w_b_rad), 0, np.sin(w_b_rad)], [0, 1, 0], [-np.sin(w_b_rad), 0, np.cos(w_b_rad)]])
        rotation_matrix_c = np.array([[1, 0, 0], [0, np.cos(w_c_rad), -np.sin(w_c_rad)], [0, np.sin(w_c_rad), np.cos(w_c_rad)]])

        # Apply rotations to ellipsoid points
        ellipsoid_points_rotated = np.dot(ellipsoid_points, rotation_matrix_a.T)
        ellipsoid_points_rotated = np.dot(ellipsoid_points_rotated, rotation_matrix_b.T)
        ellipsoid_points_rotated = np.dot(ellipsoid_points_rotated, rotation_matrix_c.T)

        # Reshape back to (100, 100, 3) and shift to the center
        ellipsoid_x, ellipsoid_y, ellipsoid_z = ellipsoid_points_rotated[:, 0].reshape(100, 100) + x, ellipsoid_points_rotated[:, 1].reshape(100, 100) + y, ellipsoid_points_rotated[:, 2].reshape(100, 100) + z

        # Plot the ellipsoid surface
        ax.plot_surface(ellipsoid_x, ellipsoid_y, ellipsoid_z, color='r', alpha=0.3)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    plt.title('3D Error Ellipsoids')
    plt.show()

# Example usage
plot_error_ellipses(data)
plot_error_ellipsoids(data)
