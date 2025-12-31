# %%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import combinations  
from itertools import product  


def plot_temperature_cubes(matrix):
    # Extracting data
    latitudes = np.array([row[0] for row in matrix])
    longitudes = np.array([row[1] for row in matrix])
    depths = np.array([row[5] for row in matrix])
    temperatures = np.array([row[6] for row in matrix])

    # Create figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Function to draw cube at each data point
    def draw_cube(x, y, z, size, color, ax):
    # Define vertices of the cube
        # scale is in the denominator so larger value = smaller face
        scale_x= 5
        scale_y= 5
        scale_z= 0.30
        vertices = np.array([
            [x - size/scale_x, y - size/scale_y, z - size/scale_z],  # Adjust depth here, seems jank but we'll see how it scales.
            [x + size/scale_x, y - size/scale_y, z - size/scale_z],
            [x + size/scale_x, y + size/scale_y, z - size/scale_z],
            [x - size/scale_x, y + size/scale_y, z - size/scale_z],
            [x - size/scale_x, y - size/scale_y, z + size/scale_z],
            [x + size/scale_x, y - size/scale_y, z + size/scale_z],
            [x + size/scale_x, y + size/scale_y, z + size/scale_z],
            [x - size/scale_x, y + size/scale_y, z + size/scale_z]
        ])

        # Define faces of the cube
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[0], vertices[3], vertices[7], vertices[4]],
            [vertices[1], vertices[2], vertices[6], vertices[5]]
        ]

        # Convert faces to Poly3DCollection
        cube = Poly3DCollection(faces, linewidths=1, edgecolors='k', alpha=0.5)
        cube.set_facecolor(color)  # Set face color
        ax.add_collection3d(cube)

    # Normalize temperature values to range [0, 1] for colormap
    norm = plt.Normalize(temperatures.min(), temperatures.max())

    # Create colormap
    cmap = plt.get_cmap('coolwarm')

    # Calculate distances between adjacent data points
    distances = np.sqrt(np.diff(latitudes)**2 + np.diff(longitudes)**2 + np.diff(depths)**2)

    # Find minimum distance
    min_distance = np.min(distances)

    # Set cube size to half of the minimum distance
    cube_size = min_distance / 10

    # Plot cubes at each data point with color corresponding to temperature
    for lat, lon, depth, temp in zip(latitudes, longitudes, depths, temperatures):
        color = cmap(norm(temp))
        draw_cube(lat, lon, depth, size=cube_size, color=color, ax=ax)

    # Set labels and title
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Depth (m)')
    ax.set_title('3D Plot of Temperature vs Depth')

    # Invert the z-axis
    ax.invert_zaxis()

    # Set axis limits
    ax.set_xlim(min(latitudes), max(latitudes))
    ax.set_ylim(min(longitudes), max(longitudes))
    ax.set_zlim(max(depths), min(depths))  # inverted depths

    # Set aspect ratio
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Temperature (°C)')

    plt.show()

# testing 3d graphs with parsed CSV data
parsed_file_path = './content/parsed/parsed_data.csv'
df_from_csv = pd.read_csv(parsed_file_path, header=None, skiprows=1)  # Read CSV and remove first row (column titles)
matrix_from_csv = df_from_csv.values.tolist()
plot_temperature_cubes(matrix_from_csv)

# %%