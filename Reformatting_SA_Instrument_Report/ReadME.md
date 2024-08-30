# Spacial Analyzer's Instrument Quick Report to Precise Planner Reformatter

This Python script processes geodesy instrument reports to extract and format measurements and coordinates from input files, and outputs the results in text files. It ensures measurements are correctly formatted, coordinates are properly renamed, and all outputs are logged to a unique file.

## Features

- Extracts instrument information and observation data from an Excel file.
- Reads coordinate data from a text file.
- Renames point IDs based on a renaming scheme to ensure uniqueness.
- Converts units for angles and distances to the desired format.
- Saves measurements and coordinates to uniquely named output files.
- Creates a log file with details of the processing and renaming operations.

## Requirements

- Python 3.x
- Required Python libraries: `pandas`, `re`, `os`, `datetime`

## Installation

1. Clone this repository or download the script files.
2. Install the required Python libraries:
    ```bash
   pip install pandas
   ```

## Usage

1. **Prepare Input Files:**
   - Place the observation data in an Excel file (e.g., `Instruments - CompositeReport.xlsx`).
   - Ensure the coordinate data is in a text file (e.g., `Point List.txt`).

2. **Run the Script:**

   Execute the script from the command line:
   ```bash
   python SA2PP.py
   ```

3. **Output Files:**
   - The script will generate three output files in the same directory as the `OBSERVATIONS_FILE`:
     - `output_measurements_<timestamp>.txt`: Contains formatted measurements.
     - `output_coordinates_<timestamp>.txt`: Contains formatted coordinates.
     - `log_file_<timestamp>.txt`: Contains the log of the operations performed.

## Configuration

### File Paths

The script uses the following file paths:

- `OBSERVATIONS_FILE`: Path to the Excel file containing observation data.
- `COORDINATES_FILE`: Path to the text file containing coordinate data.

These paths are defined at the beginning of the script:
```python
OBSERVATIONS_FILE = 'V:\\Projekte\\PETRA4\\Simulationen\\Girder alignment\\Instruments - CompositeReport.xlsx'
COORDINATES_FILE = 'V:\\Projekte\\PETRA4\\Simulationen\\Girder alignment\\Point List.txt'
```

### Output Files

Output files are generated with a timestamp to avoid overwriting:
```python
OUTPUT_MEASUREMENTS_FILE = os.path.join(output_directory, f'output_measurements_{timestamp}.txt')
OUTPUT_COORDINATES_FILE = os.path.join(output_directory, f'output_coordinates_{timestamp}.txt')
LOG_FILE = os.path.join(output_directory, f'log_file_{timestamp}.txt')
```

### Units Configuration

The script expects angles to be in `gon` and distances in `mm`. These units are extracted from the input files and converted if necessary.

## Logging

A log file is created during the script execution to record the processing steps. The log file includes:

- Number of instruments detected.
- Units extracted for measurements.
- Any errors or warnings encountered during processing.
- The renaming key for coordinates.

The log file is saved with a unique name (`log_file_<timestamp>.txt`) to prevent overwriting previous logs.

## Error Handling

The script includes error handling for:

- Missing or invalid data.
- Conflicts in point IDs.
- File read/write errors.

If an error occurs, the script logs the error and continues processing where possible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For questions or support, please contact the author at [jana.barker@desy.de].
