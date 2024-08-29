import pandas as pd
import re
import os

# --------------------- Configuration Section ---------------------
# Constants and configurable settings

# Precision settings
ZENITHAL_ANGLE_PRECISION = 0.00015
DIRECTION_PRECISION = 0.00015
SLOPE_DISTANCE_PRECISION_CONSTANT = 0.03903  # Fixed part of slope distance precision
SLOPE_DISTANCE_PRECISION_VARIABLE = 1e-6     # Variable part of slope distance precision



# Precision settings
ZENITHAL_ANGLE_PRECISION = 0.00015
DIRECTION_PRECISION = 0.00015
SLOPE_DISTANCE_PRECISION_CONSTANT = 0.0102  # Fixed base value (constant) for slope distance precision
SLOPE_DISTANCE_PRECISION_VARIABLE = 15e-6     # Variable part for slope distance precision per unit distance

# Expected units for validation and conversion
UNIT_ANGLES = 'gon'     # Expected unit for angles ('gon', 'rad', 'mrad', 'deg')
UNIT_DISTANCES = 'mm'   # Expected unit for distances ('m', 'cm', 'mm', 'um')

# File paths
script_directory = os.path.dirname(os.path.abspath(__file__))
OBSERVATIONS_FILE = 'V:\Projekte\PETRA4\Simulationen\Girder alignment\Instruments - CompositeReport.xlsx'  # Path to the Excel file with observations
COORDINATES_FILE = 'V:\Projekte\PETRA4\Simulationen\Girder alignment\Point List.txt'                      # Path to the text file with coordinates

# Output files
OUTPUT_MEASUREMENTS_FILE = os.path.join(script_directory, 'output_measurements.txt')
OUTPUT_COORDINATES_FILE = os.path.join(script_directory, 'output_coordinates.txt')
LOG_FILE = os.path.join(script_directory, 'log_file.txt')

# Toggle to print the log to the terminal
PRINT_LOG_TO_TERMINAL = True

# --------------------- Function Definitions ---------------------

def log_message(message, log_data, print_to_terminal=True):
    """
    Logs a message to the log data list and optionally prints it to the terminal.
    """
    log_data.append(message)
    if PRINT_LOG_TO_TERMINAL and print_to_terminal:
        print(message)

def extract_instrument_number(instrument_info, line_number):
    """
    Extracts the instrument number from the format Collection_name::InstrumentID - Manufacturer.
    Adds 4000 to the InstrumentID to generate the station number.
    Raises an error with the line number if extraction fails.
    """
    try:
        instrument_id = int(instrument_info.split("::")[1].split(" - ")[0].strip())
        station_number = instrument_id + 4000
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error extracting instrument number on line {line_number + 1}: {e}")
    return station_number

def find_instrument_and_observations(file_path, log_data):
    """
    Reads the Excel file and finds where each instrument and its observations start.
    Extracts instrument information and the corresponding observations.
    """
    xls = pd.ExcelFile(file_path)
    data = xls.parse(xls.sheet_names[0])  # Read the entire sheet

    instrument_info = []
    observation_sections = []

    # Locate instrument sections and observations sections
    for index, row in data.iterrows():
        # Identify the start of instrument information using the "Transform" keyword
        if isinstance(row.iloc[0], str) and row.iloc[0].startswith("Transform"):
            instrument_name = data.iloc[index, 0]
            log_message(f"Found instrument line at row {index + 1}: {instrument_name}", log_data)

            # Extract the measurement count from the next column in the same row
            meas_row = data.iloc[index + 1, 0]
            if isinstance(meas_row, str) and "# Meas." in meas_row:
                try:
                    meas_count = int(data.iloc[index + 1, 1])  # Correct to take the count from the next column
                    station_number = extract_instrument_number(instrument_name, index)
                    instrument_info.append((instrument_name, meas_count, index, station_number))
                    log_message(f"Instrument added: {instrument_name} (Station Number: {station_number})", log_data)
                except ValueError as e:
                    log_message(f"Error extracting measurement count for {instrument_name} at line {index + 2}: {e}", log_data)

        # Identify where observations start and end at the next instrument or section end
        if isinstance(row.iloc[0], str) and row.iloc[0].startswith("Observations"):
            obs_instrument_name = data.iloc[index, 0]
            log_message(f"Found observations for instrument: {obs_instrument_name}", log_data)
            header_row = index + 1  # Row immediately after "Observations" contains the column names
            observations_start = header_row + 1  # Data starts after the header

            # Find the end of the observation section until next instrument
            observations_end = len(data)
            for obs_index in range(observations_start, len(data)):
                if isinstance(data.iloc[obs_index, 0], str) and data.iloc[obs_index, 0].startswith("Transform"):
                    observations_end = obs_index
                    break

            # Extract the relevant section of observations between start and end
            observations = data.iloc[observations_start:observations_end]

            # Log actual column names to ensure proper extraction
            log_message(f"Column names identified in section: {observations.columns.tolist()}", log_data)

            # Append the extracted observations
            observation_sections.append((obs_instrument_name, observations, station_number))

    # Match data format and consistent units
    matched_data = [(name, station_number, observations) for name, observations, station_number in observation_sections]

    log_message(f"Total Instruments Detected: {len(instrument_info)}", log_data)
    return matched_data, {}

def read_coordinates(file_path, log_data):
    """
    Reads coordinates from a text file and processes them into a dictionary.
    """
    coords = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('//') or not line.strip():
                continue  # Skip comments and empty lines
            parts = line.strip().split(',')
            point_name = parts[0].strip()
            coords[point_name] = [float(x.strip()) for x in parts[1:]]
    log_message(f"Coordinates successfully read from {file_path}.", log_data)
    return coords

def angle_to_gon(unit):
    """
    Converts an angle unit to gon.

    Parameters:
    - unit (str): The angle unit to be converted.

    Returns:
    - float: Conversion factor to gon.

    Raises:
    - ValueError: If the input unit is not recognized.
    """
    if unit == "gon":
        return 1.0
    elif unit == "rad":
        return 200 / 3.141592653589793
    elif unit == "mrad":
        return 200 / 3.141592653589793 / 1000
    elif unit == "deg":
        return 200 / 180
    else:
        raise ValueError(f"Invalid angle unit specified: {unit}")

def distance_to_mm(unit):
    """
    Converts a distance unit to millimeters.

    Parameters:
    - unit (str): The distance unit to be converted.

    Returns:
    - float: Conversion factor to millimeters.

    Raises:
    - ValueError: If the input unit is not recognized.
    """
    if unit == "um":
        return 0.001
    elif unit == "mm":
        return 1.0
    elif unit == "cm":
        return 10.0
    elif unit == "m":
        return 1000.0
    else:
        raise ValueError(f"Invalid distance unit specified: {unit}")

def create_renaming_scheme(coordinates):
    """
    Creates a renaming scheme based on the coordinate file.
    Checks for conflicts with instrument IDs and raises errors if issues are detected.
    """
    renaming_key = {}
    unique_id = 1

    # Create renaming scheme for all coordinate points
    for point_name in coordinates.keys():
        if point_name not in renaming_key:
            renaming_key[point_name] = unique_id
            unique_id += 1

    return renaming_key

def check_instrument_conflicts(instruments, renaming_key):
    """
    Checks if any instrument IDs conflict with existing point IDs.
    Raises an error if conflicts are found.
    """
    instrument_ids = {id + 4000 for id, _ in instruments}
    conflicting_ids = set(renaming_key.values()) & instrument_ids

    if conflicting_ids:
        raise ValueError(f"Conflicting IDs found between instruments and points: {conflicting_ids}")

def process_data(observations, coordinates, station_number, renaming_key, log_data, units):
    """
    Processes observations to create the required outputs, without saving coordinates from measurements.
    """
    measurements_output = []

    # Precision configuration for measurement types with rounding for sd
    precision_config = {
        'zu': ZENITHAL_ANGLE_PRECISION,
        'di': DIRECTION_PRECISION,
        'sd': lambda dist: round(SLOPE_DISTANCE_PRECISION_CONSTANT + (SLOPE_DISTANCE_PRECISION_VARIABLE * dist), 5)
    }

    # Check and rename measurements according to the renaming scheme
    for _, row in observations.iterrows():
        target = str(row.iloc[2])  # Access Column C for the target

        if target not in renaming_key:
            log_message(f"Error: Measurement target '{target}' not found in coordinates file.", log_data)
            raise ValueError(f"Measurement target '{target}' not found in coordinates file.")

        target_number = renaming_key[target]  # Get the renamed numeric ID

        try:
            azimuth = float(str(row.iloc[3]).replace(',', '.'))  # Column D
            elevation = float(str(row.iloc[4]).replace(',', '.'))  # Column E
            distance = float(str(row.iloc[5]).replace(',', '.'))  # Column F
        except ValueError:
            log_message(f"Invalid measurement data for target {target}, skipping row.", log_data)
            continue

        # First type: Measurement information with calculated precision
        measurements_output.append(f"zu {station_number} {target_number} {precision_config['zu']}")
        measurements_output.append(f"di {station_number} {target_number} {precision_config['di']}")
        measurements_output.append(f"sd {station_number} {target_number} {precision_config['sd'](distance)}")

    return measurements_output

def extract_instrument_coordinates(data, index):
    """
    Extracts the instrument coordinates and units from the specified rows.
    """
    print(data[index])
    # Extract coordinates from columns D, E, F
    x_coord = float(data.iloc[index, 3])  # Column D
    y_coord = float(data.iloc[index, 4])  # Column E
    z_coord = float(data.iloc[index, 5])  # Column F

    # Extract units from column C
    #units = str(data.iloc[index, 2]).strip()  # Column C for units

    return (x_coord, y_coord, z_coord)

def save_coordinates(coordinates, renaming_key, instrument_coords, file_name):
    """
    Saves the coordinates from the coordinates file along with instrument coordinates into a file.
    """
    with open(file_name, 'w') as file:
        # Save coordinates from the coordinates file
        for original_name, coord in coordinates.items():
            target_number = renaming_key.get(original_name, original_name)  # Get renamed numeric ID or keep the original name
            file.write(f"{target_number} {coord[0]} {coord[1]} {coord[2]}\n")
        
        # Save instrument coordinates
        for instr_name, (x, y, z) in instrument_coords.items():
            file.write(f"{instr_name} {x} {y} {z} \n")#({units})

    print(f"Coordinates saved to {file_name}")

def save_to_file(data, file_name):
    """
    Saves a list of strings to a text file.
    """
    with open(file_name, 'w') as file:
        file.write('\n'.join(data))

def save_log(log_data, renaming_key, file_name):
    """
    Saves the log data and renaming key to a file.
    """
    with open(file_name, 'w') as file:
        # Write log data
        file.write('\n'.join(log_data))
        file.write('\n\nRenaming Key:\n')
        
        # Format and write renaming key
        for original_name, numeric_id in renaming_key.items():
            file.write(f"{original_name} -> {numeric_id}\n")

# --------------------- Script Execution ---------------------

# Initialize log data
log_data = []

# Step 1: Read instrument and observation data
matched_data, units = find_instrument_and_observations(OBSERVATIONS_FILE, log_data)
if matched_data is None:
    log_message("Error in finding instruments and observations.", log_data)
else:
    # Step 2: Read coordinates and create renaming scheme
    coordinates = read_coordinates(COORDINATES_FILE, log_data)
    renaming_key = create_renaming_scheme(coordinates)

    # Extract instrument coordinates for saving later
    instrument_coords = {}
    for instr_name, station_number, observations in matched_data:
        index = observations.index.start - 2  # Adjust based on the starting index of the instrument data
        instrument_coords[instr_name] = extract_instrument_coordinates(OBSERVATIONS_FILE, index)

    # Check for instrument ID conflicts with the renaming scheme
    instruments = [(index, instr_name) for index, (instr_name, station_number, observations) in enumerate(matched_data)]
    check_instrument_conflicts(instruments, renaming_key)

    measurements_output = []

    # Step 3: Process each instrument's observations
    for instr_name, station_number, observations in matched_data:
        try:
            # Process the observations to get measurements
            instr_measurements = process_data(
                observations, coordinates, station_number, renaming_key, log_data, units
            )
            measurements_output.extend(instr_measurements)

        except ValueError as e:
            log_message(str(e), log_data)

    # Step 4: Save the processed data and coordinates
    save_to_file(measurements_output, OUTPUT_MEASUREMENTS_FILE)
    save_coordinates(coordinates, renaming_key, instrument_coords, OUTPUT_COORDINATES_FILE)
    log_message(f"Saved measurements to {OUTPUT_MEASUREMENTS_FILE}", log_data)
    log_message(f"Saved coordinates to {OUTPUT_COORDINATES_FILE}", log_data)

    # Save the log file along with the renaming key
    save_log(log_data, renaming_key, LOG_FILE)
    log_message(f"Log saved to {LOG_FILE}", log_data)