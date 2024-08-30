from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import numpy as np

def plot_ellipsoid(cov_matrix, mean, ax=None, n_std=1.0):
    """
    Plots an error ellipsoid based on a covariance matrix.

    :param cov_matrix: 3x3 covariance matrix
    :param mean: Center of the ellipsoid (mean of the data)
    :param ax: Matplotlib 3D axis object
    :param n_std: Number of standard deviations to determine the ellipsoid's radii
    """
    if ax is None:
        ax = plt.gca(projection='3d')

    # Eigenvalue decomposition
    eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)

    # Scaling factors for the ellipsoid radii
    radii = n_std * np.sqrt(eigenvals)

    # Generate data for the ellipsoid
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radii[0] * np.outer(np.cos(u), np.sin(v))
    y = radii[1] * np.outer(np.sin(u), np.sin(v))
    z = radii[2] * np.outer(np.ones_like(u), np.cos(v))

    # Rotate data to align with the eigenvectors
    ellipsoid_points = np.dot(np.column_stack((x.ravel(), y.ravel(), z.ravel())), eigenvecs.T).reshape(x.shape)
    x, y, z = ellipsoid_points[:, :, 0] + mean[0], ellipsoid_points[:, :, 1] + mean[1], ellipsoid_points[:, :, 2] + mean[2]

    ax.plot_surface(x, y, z, color='r', alpha=0.3)

# Example usage
cov_matrix = np.array([[5, 2, 1], [2, 3, 1], [1, 1, 4]])  # Sample 3x3 covariance matrix
mean = [0, 0, 0]  # Mean or center point

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plot_ellipsoid(cov_matrix, mean, ax, n_std=2)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.title('3D Error Ellipsoid')
plt.show()