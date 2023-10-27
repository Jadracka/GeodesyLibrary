import os
import subprocess
import time
import psutil
import re

SpatialAnalyzer = r"C:\Program Files (x86)\New River Kinematics" \
    r"\SpatialAnalyzer 2023.2.0926.5\x64\Spatial Analyzer64.exe"

def start_program(program_path, timeout=6):
    try:
        subprocess.Popen(f'"{program_path}"', shell=True)

        time.sleep(timeout)  # Wait for the program to start (you might need to adjust the delay)

        program_name = os.path.basename(program_path)
        for proc in psutil.process_iter(attrs=['name']):
            if proc.info['name'] == program_name:
                return True  # Program started successfully

    except (subprocess.CalledProcessError, Exception):
        pass

    return False  # Program did not start or an error occurred

def is_program_running(program_name):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == program_name:
            return True
    return False

if os.path.exists(SpatialAnalyzer):
    # print(f"The file at {SpatialAnalyzer} exists. Starting SA.")
    status = start_program(SpatialAnalyzer)
    if status:
        print("SA Started.")
        
else:
    # Define the directory where you want to search for the executable file
    search_directory = "C:\\"
    print(f"I'm searching for Spatial Analyzer in {search_directory}.\n \
    You may consider updating the file path to SpatialAnalyzer variable \n \
    to make the next startup faster.")

    pattern = re.compile(r"(?=.*Spatial)(?=.*Analyzer)(?!.*Installer)"
                    r"(?!.*UDP)(?!.*SDK).*\.exe$", re.I)

    matching_paths = []

    # Loop through the files in the directory and its subdirectories
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if pattern.match(file):
                # Check if the file's title contains both words, no "Installer," and has a .exe extension
                file_path = os.path.join(root, file)
                matching_paths.append(file_path)

    if len(matching_paths) == 1:
        # Only one matching file found, execute it
        print(f"Your SA path is: {matching_paths[0]}")
        
        status = start_program(matching_paths[0])
        if status:
            print("SA Started.")

    elif len(matching_paths) > 1:
        # Multiple matching files found, notify the user
        print("Multiple SA instances found. Please update the file path with the desired version.")
        print("SA paths:")
        for path in matching_paths:
            print(path)
        
    else:
        # No matching files found
        print("No SA found. Try updating SA path in the variable.")