# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:19:29 2023

@author: jbarker
"""

import os

def read_text_file(file_path):
    data_dict = {}
    
    # Extract the file name (without extension) from the file path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 4:
                point_name = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                data_dict[point_name] = (x, y, z)
    
    return {file_name: data_dict}

# Replace 'your_data.txt' with the path to your text file
file_path = 'your_data.txt'

resulting_dict = read_text_file(file_path)
print(resulting_dict)
