#%%
import math
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sqlite3
import pandas as pd
from ipywidgets import widgets, interact

# Function to query data by date range
def query_data_by_date_range(db_file, start_date, end_date, min_latitude, max_latitude, min_longitude, max_longitude, depth_bin_size=100, depth_limit = 10000):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # num_bins = math.ceil(5000 / depth_bin_size)  # Assuming the maximum depth is 5000m

        # Prepare the SQL query with depth binning
        query = f'''
        SELECT
            Latitude,
            Longitude,
            Year,
            Month,
            Day,
            (CAST(Depth_bin / {depth_bin_size} AS INTEGER) * {depth_bin_size}) AS Depth_bin,  -- Binning depth into 100m increments
            AVG(Temperature) as Temperature
        FROM 
            cast_data
        WHERE 
            (Year || '-' || printf('%02d', Month) || '-' || printf('%02d', Day)) BETWEEN ? AND ?
            AND Latitude BETWEEN ? AND ?
            AND Longitude BETWEEN ? AND ?
            AND Depth_bin < {depth_limit}
        GROUP BY
            Latitude, Longitude, Year, Month, Day, (CAST(Depth_bin / {depth_bin_size} AS INTEGER) * {depth_bin_size});
        '''
        # Execute the query with parameters
        cursor.execute(query, (start_date, end_date, min_latitude, max_latitude, min_longitude, max_longitude))
        
        # Fetch all results
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert the results to a DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        # Ensure the connection is closed even if an error occurs
        if conn:
            conn.close()

# Function to plot temperature cubes
def plot_temperature_cubes(df):
    # Extracting data
    latitudes = df['Latitude'].values
    longitudes = df['Longitude'].values
    depths = df['Depth_bin'].values
    temperatures = df['Temperature'].values

    # Create figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Function to draw cube at each data point
    def draw_cube(x, y, z, size, color, ax):
        # Define vertices of the cube
        scale_x = 100
        scale_y = 100
        scale_z = 0.5
        vertices = np.array([
            [x - size/scale_x, y - size/scale_y, z - size/scale_z],
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
    ax.set_title(f'3D Plot of Temperature vs Depth ({start_date} to {end_date})')

    # Invert the z-axis
    ax.invert_zaxis()

    # Set axis limits
    ax.set_xlim(min(latitudes) - 0.15, max(latitudes) + 0.15)
    ax.set_ylim(min(longitudes) + 0.15, max(longitudes) - 0.15)
    ax.set_zlim(max(depths) + depth_bin_size, min(depths))  # inverted depths

    # Set aspect ratio
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Temperature (°C)')

    plt.show()


if __name__ == "__main__":
    # Path to your database file
    db_file = '/home/jpforbes/workspace/github.com/jpforbes5151/csvScraper/database/oceandata.db'  # Replace with the path to your database file
    
    '''
    # Ask for date range
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    min_latitude = input("Enter the Minimum latitude: ")
    max_latitude = input("Enter the Maximum latitude: ")
    min_longitude = input("Enter the Minimum longitude: ")
    max_longitude = input("Enter the Maximum longitude: ")
    '''

    # explicitly state the start and end date
    start_date = '2000-01-01'
    end_date = '2023-09-01'
    min_latitude = '50'
    max_latitude = '51'
    min_longitude = '-42'
    max_longitude =  '-40'

    ## --------------- OVERRIDE DEFAULT PARAMS ------------------
    #Depth bin size
    depth_bin_size = 100

    #max depth on queried data and plot
    depth_limit = 1000

    ##--------- END OVERRIDE PARAMS ---------------------------

    # Validate the date format
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Ensure start_date is before end_date
        if start_date > end_date:
            raise ValueError("Start date must be before end date.")
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Ensure latitude range is input correctly
        if int(min_latitude) > int(max_latitude):
            raise ValueError("The Minimum Latitude must be larger than the Maximum Latitude being input.")

        # Ensure longitude range is input correctly
        if int(min_longitude) > int(max_longitude):
            raise ValueError("The Minimum Longitude must be larger than the Maximum Longitude being input.")

        

        # Query the database
        result_df = query_data_by_date_range(db_file, start_date_str, end_date_str, min_latitude, max_latitude, min_longitude, max_longitude, depth_bin_size, depth_limit)
        if result_df is not None and not result_df.empty:
            print("Query Results:")
            print(result_df)
            # Plot the results
            plot_temperature_cubes(result_df)
        else:
            print("No data found for the given date range.")

    except ValueError as e:
        print(f"Invalid date format or range: {e}")
# %%
