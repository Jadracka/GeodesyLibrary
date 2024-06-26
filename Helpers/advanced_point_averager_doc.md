# Point Aggregation and Combination Algorithm

## Overview

This algorithm processes multiple text files containing point data, aggregates the data, and computes weighted averages and combined covariance matrices for each unique point. The results include new coordinates, standard deviations, and source information for each point. Finally, the points are sorted based on a combined standard deviation (`Sigma_XY`) and printed.

## Input File Format

Each text file should contain point data in the following format:

PoID, X[mm], Y[mm], Z[mm], Sigma_X, Sigma_Y, Sigma_Z, Sigma_{mag}, Cov_0_0, Cov_0_1, Cov_0_2, Cov_1_0, Cov_1_1, Cov_1_2, Cov_2_0, Cov_2_1, Cov_2_2


- **PoID**: Point ID (string)
- **X, Y, Z**: Coordinates in mm
- **Sigma_X, Sigma_Y, Sigma_Z**: Coordinate standard deviations
- **Sigma_mag**: Standard deviation of the magnitude
- **Cov_ij**: Elements of a 3x3 covariance matrix

## Algorithm Steps

### 1. Reading Point Data

**Function**: `read_point_file(file_path)`

Reads point data from a text file and returns a dictionary of points.

- **Args**:
  - `file_path` (str): Path to the text file containing point data.
- **Returns**:
  - `dict`: Dictionary where keys are point IDs (PoID) and values are dictionaries containing coordinates, sigmas, sigma_mag, and covariance matrix for each point.

### 2. Aggregating Points

**Function**: `aggregate_points(file_paths)`

Aggregates points from multiple files into a single dictionary.

- **Args**:
  - `file_paths` (list): List of file paths containing point data.
- **Returns**:
  - `dict`: Dictionary where keys are point IDs (PoID) and values are lists of point data dictionaries from each file.

### 3. Combining Points

**Function**: `combine_points(all_points)`

Combines instances of each point using the weighted averaging algorithm and calculates new coordinates, covariance matrices, and standard deviations.

- **Args**:
  - `all_points` (dict): Dictionary where keys are point IDs (PoID) and values are dictionaries with instances of point data and the sources they came from.
- **Returns**:
  - `dict`: Dictionary where keys are point IDs (PoID) and values are dictionaries containing new coordinates, combined covariance matrix, standard deviations, number of instances, and sources of each point.

### 4. Printing Sorted Points

**Function**: `print_sorted_points(combined_points)`

Prints the points sorted by their combined `Sigma_XY`.

- **Args**:
  - `combined_points` (dict): Dictionary where keys are point IDs (PoID) and values are dictionaries containing point data.
