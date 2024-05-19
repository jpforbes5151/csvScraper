#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import combinations  
from itertools import product  

## Visualization functions
def plot_depth_vs_temperature(matrix):
    # print what is received
    print("Received Matrix:")
    print(matrix)

    df = pd.DataFrame(matrix, columns=['Latitude', 'Longitude', 'Year', 'Month', 'Day', 'Depth', 'Temperature', 'Salinity'])
    
    #test frame output
    print("this is the data frame when generated:")
    print(df)

    #convert Depth and Temperature columns to numeric values
    df['Depth'] = pd.to_numeric(df['Depth'])
    df['Temperature'] = pd.to_numeric(df['Temperature'])

    #make the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Temperature'], df['Depth'], marker='o', linestyle='-', color='b')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Depth (m)')
    plt.title('Depth vs Temperature')
    plt.gca().invert_yaxis()  # Invert the y-axis to show depth increasing downwards
    #plt.gca().invert_xaxis()  # Invert the x-axis to show depth decreasing from left to right
    plt.show()
    print("this is the data frame after generating the plot:", df)

def plot_depth_vs_salinity(matrix):
    df = pd.DataFrame(matrix, columns=['Latitude', 'Longitude', 'Year', 'Month', 'Day', 'Depth', 'Temperature', 'Salinity'])
    df['Depth'] = pd.to_numeric(df['Depth'])
    df['Salinity'] = pd.to_numeric(df['Salinity'])

    plt.figure(figsize=(10, 6))
    plt.plot(df['Salinity'], df['Depth'], marker='o', linestyle='-', color='g')
    plt.xlabel('Salinity (PSS)')
    plt.ylabel('Depth (m)')
    plt.title('Depth vs Salinity')
    plt.gca().invert_yaxis()  # Invert the y-axis to show depth increasing downwards
    #plt.gca().invert_xaxis()  # Invert the x-axis to show depth decreasing from left to right
    plt.show()

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
        vertices = np.array([
            [x - size, y - size, z - size],
            [x + size, y - size, z - size],
            [x + size, y + size, z - size],
            [x - size, y + size, z - size],
            [x - size, y - size, z + size],
            [x + size, y - size, z + size],
            [x + size, y + size, z + size],
            [x - size, y + size, z + size]
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

    # Plot cubes at each data point with color corresponding to temperature
    for lat, lon, depth, temp in zip(latitudes, longitudes, depths, temperatures):
        color = cmap(norm(temp))
        draw_cube(lat, lon, depth, size=1, color=color, ax=ax)

    # Set labels and title
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Depth (m)')
    ax.set_title('3D Plot of Temperature (Cubes)')

    # Invert the z-axis
    ax.invert_zaxis()

    # Set axis limits
    ax.set_xlim(min(latitudes), max(latitudes))
    ax.set_ylim(min(longitudes), max(longitudes))
    ax.set_zlim(max(depths), min(depths)) #inverted depths

    # Set aspect ratio
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Temperature (°C)')

    plt.show()


#### optional things

# Function to read CSV and remove header
'''
def read_csv_without_header(file_path):
    df = pd.read_csv(file_path, skiprows=1)  # Skip the header row
    return df
'''
## testing the plots

#testing with explicit data:
'''
test_matrix = [
    [44.565, -63.9917, 1969, 7, 2, 9.92, 14.9, 31.23],
    [44.565, -63.9917, 1969, 7, 2, 19.84, 5, 31.34],
    [44.565, -63.9917, 1969, 7, 2, 29.76, 3.8, 31.5],
    [44.565, -63.9917, 1969, 7, 2, 49.59, 3.6, 31.53]
]
plot_depth_vs_temperature(test_matrix)
'''


####

#testing 2d graphs with parsed CSV data
'''
parsed_file_path = './content/parsed/parsed_data_8.csv'
df_from_csv = pd.read_csv(parsed_file_path, header=None, skiprows=1)  # Read CSV and remove first row (column titles)
matrix_from_csv = df_from_csv.values.tolist()
plot_depth_vs_temperature(matrix_from_csv)
plot_depth_vs_salinity(matrix_from_csv)
'''

# testing 3d graphs with parsed CSV data

parsed_file_path = './content/parsed/parsed_data.csv'
df_from_csv = pd.read_csv(parsed_file_path, header=None, skiprows=1)  # Read CSV and remove first row (column titles)
matrix_from_csv = df_from_csv.values.tolist()
plot_temperature_cubes(matrix_from_csv)

# %%
