import csv
import os
from datetime import datetime
import pandas as pd

def parse_casts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    casts = []
    cast = None
    variables_section = False

    for line in lines:
        # Check for new cast section
        if line.startswith("#--------------------------------------------------------------------------------"):
            if cast:
                casts.append(cast)
            cast = {'metadata': {}, 'variables': []}
            variables_section = False

        # Check if the line is a metadata line
        elif cast is not None and not variables_section:
            if 'VARIABLES' in line:
                variables_section = True
            else:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) > 2 and parts[2]:
                    key = parts[0].strip()
                    value = parts[2].strip()
                    cast['metadata'][key] = value

        # Process the variables section
        elif variables_section:
            if 'END OF VARIABLES SECTION' in line:
                variables_section = False
            else:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) > 3:
                    depth = parts[1]
                    temperature = parts[4]
                    salinity = parts[7]
                    cast['variables'].append([depth, temperature, salinity])

    # Add the last cast
    if cast:
        casts.append(cast)

    return casts

def create_matrix(casts):
    matrix = []

    for cast in casts:
        metadata = cast['metadata']
        variables = cast['variables']
        for var in variables:
            depth = var[0]
            temperature = var[1]
            salinity = var[2]

            # Check if any of the variables are null or NaN
            if depth != '' and temperature != '' and salinity != '' and \
               not pd.isnull(depth) and not pd.isnull(temperature) and not pd.isnull(salinity):
                row = [
                    metadata.get('Latitude', ''),
                    metadata.get('Longitude', ''),
                    metadata.get('Year', ''),
                    metadata.get('Month', ''),
                    metadata.get('Day', ''),
                    depth,        # Depth
                    temperature,  # Temperature
                    salinity      # Salinity
                    # Add more elements here if necessary
                ]
                matrix.append(row)

    return matrix

def write_to_csv(matrix, output_file):
    # Check if the file already exists
    if os.path.exists(output_file):
        # Append timestamp to the filename
        base, ext = os.path.splitext(output_file)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{base}_{timestamp}{ext}"

    header = ['Latitude', 'Longitude', 'Year', 'Month', 'Day', 'Depth', 'Temperature', 'Salinity']

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(matrix)

    print(f'Data parsed and written to {output_file}')


# Example usage
input_file = './content/ocldb1571108899.16715.CTD2.csv'
output_file = './content/parsed/parsed_data.csv'

casts = parse_casts(input_file)
matrix = create_matrix(casts)
write_to_csv(matrix, output_file)


