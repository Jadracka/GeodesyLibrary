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
filename = 'Helpers\Channels_3000.csv'
print_last_line_with_number(filename)
filename = 'Helpers\Channels_300.csv'
print_last_line_with_number(filename)