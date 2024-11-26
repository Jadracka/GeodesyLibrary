import csv

def print_last_line_with_number(filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        last_line = None
        line_number = 0
        
        for line_number, row in enumerate(reader, start=1):
            last_line = row
        
        if last_line is not None:
            print(f"Last line number: {line_number}")
            print(f"Last line content: {','.join(last_line)}")
        else:
            print("The file is empty.")

# Replace 'yourfile.csv' with the path to your CSV file.
filename = 'V:/Projekte/PETRA4/Pillar stability Tests/06Aug24 Instrument Stand Prototype 0 - LT_Arm_Seismo/Channels_300.csv'
print_last_line_with_number(filename)
filename = 'V:/Projekte/PETRA4/Pillar stability Tests/06Aug24 Instrument Stand Prototype 0 - LT_Arm_Seismo/Channels.csv'
print_last_line_with_number(filename)