import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame containing the CSV data.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        ValueError: If there is an issue parsing the CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except ValueError as e:
        raise ValueError(f"Error parsing the file: {e}")


def filter_bike_counters(data: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the DataFrame to keep only rows related to bike counters.

    Args:
        data (pd.DataFrame): The DataFrame containing counters data.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only bike counters.
    """
    return data[data['Nom du com'].str.contains('Vélo', na=False)]


def extract_bike_counter_locations(data: pd.DataFrame) -> dict:
    """
    Extract bike counter locations (latitude and longitude) from a DataFrame.

    Args:
        data (pd.DataFrame): The filtered DataFrame containing bike counter data.

    Returns:
        dict: A dictionary where keys are counter names and values are tuples (latitude, longitude).
    """
    locations = {}
    for index, row in data.iterrows():
        name = row['Nom du com']
        lat = row['Latitude']
        lon = row['Longitude']
        locations[name] = (lat, lon)
    return locations


if __name__ == "__main__":
    # Path to the CSV file
    CSV_FILE_PATH = 'data/MMM_MMM_GeolocCompteurs.csv'

    # Step 1: Load the CSV file
    try:
        data = load_csv(CSV_FILE_PATH)
        print("CSV file loaded successfully.")
        print(data.head())  # Display the first rows of the DataFrame
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading the CSV file: {e}")
        exit()

    # Step 2: Filter data for bike counters
    bike_counters_data = filter_bike_counters(data)
    print("Filtered data for bike counters:")
    print(bike_counters_data.head())  # Display the first rows of the filtered DataFrame

    # Step 3: Extract bike counter locations
    bike_counter_locations = extract_bike_counter_locations(bike_counters_data)
    print("Bike counter locations extracted:")
    print(bike_counter_locations)

