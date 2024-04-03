import csv
import os

# Sample data in the form of a dictionary
data = {
    'Name': ['juan', 'Bob', 'Charlie'],
    'Age': [25, 30, 22],
    'Country': ['USA', 'Canada', 'UK'],
    "Chela fav": ["Modelo","Tecate","Indio","Corona"]
}

# Specify the CSV file name
csv_file = 'data.csv'

# Check if the CSV file already exists
if os.path.exists(csv_file):
    # If the file exists, read the existing headers
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        existing_headers = next(reader, [])
        print(existing_headers)

    # Check if any of the headers in data already exist
    headers_to_add = [header for header in data.keys() if header not in existing_headers]
    if headers_to_add:
     existing_headers.append(headers_to_add[0])
    print(existing_headers)

else:
    # If the file doesn't exist, add all headers
    headers_to_add = data.keys()


# Open the CSV file in write mode (either create a new file or append to an existing file)
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)

    # If the file is new or any headers are new, write the header row
    if not os.path.exists(csv_file) or headers_to_add:
        writer.writerow(headers_to_add)

    # Write the data rows
    rows = zip(*[data.get(header, [""] * len(data["Name"])) for header in existing_headers])
    writer.writerows(rows)

print(f"CSV file '{csv_file}' updated successfully.")