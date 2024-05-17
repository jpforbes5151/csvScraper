#%%

import matplotlib.pyplot as plt
import pandas as pd

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
    plt.gca().invert_xaxis()  # Invert the x-axis to show depth decreasing from left to right
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
#testing with parsed CSV data
parsed_file_path = './content/parsed/parsed_data.csv'
df_from_csv = pd.read_csv(parsed_file_path, header=None, skiprows=1)  # Read CSV and remove first row (column titles)
matrix_from_csv = df_from_csv.values.tolist()
plot_depth_vs_temperature(matrix_from_csv)
plot_depth_vs_salinity(matrix_from_csv)



# %%
