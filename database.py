import pandas as pd
import sqlite3

def create_and_populate_db(csv_file, db_file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Create a new SQLite database (or connect to an existing one)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create a table with appropriate schema
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS cast_data (
            Latitude REAL,
            Longitude REAL,
            Year INTEGER,
            Month INTEGER,
            Day INTEGER,
            Depth_bin REAL,
            Temperature REAL,
            Salinity REAL
        )
        '''
        cursor.execute(create_table_query)
        conn.commit()

        # Insert the DataFrame data into the SQLite table
        df.to_sql('cast_data', conn, if_exists='append', index=False)

        print("Data has been written to the local database successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the connection is closed even if an error occurs
        if conn:
            conn.close()

# Example usage
'''
csv_file = '/home/jpforbes/workspace/github.com/jpforbes5151/csvScraper/content/parsed/parsed_data_6.csv'  # Replace with the actual path to your CSV file
db_file = '/home/jpforbes/workspace/github.com/jpforbes5151/csvScraper/database/oceandata.db'  # Replace with the path where you want to store the database file
create_and_populate_db(csv_file, db_file)
'''

'''
def query_data_by_date_range(db_file, start_date, end_date):
    """
    Query data from the database within a specified date range.

    :param db_file: Path to the SQLite database file.
    :param start_date: Start date in 'YYYY-MM-DD' format.
    :param end_date: End date in 'YYYY-MM-DD' format.
    :return: DataFrame containing the queried data.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Prepare the SQL query
        query = '''
        #SELECT * FROM cast_data
        #WHERE (Year || '-' || Month || '-' || Day) BETWEEN ? AND ?
'''
        # Execute the query with parameters
        cursor.execute(query, (start_date, end_date))
        
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

# Example usage
if __name__ == "__main__":
    db_file = '/home/jpforbes/workspace/github.com/jpforbes5151/csvScraper/database/oceandata.db'  # Replace with the path to your database file
    start_date = '2003-10-01'  # Replace with your start date (YY-MM-DD)
    end_date = '2003-10-31'    # Replace with your end date (YY-MM-DD)

    result_df = query_data_by_date_range(db_file, start_date, end_date)
    if result_df is not None:
        print(result_df)

'''