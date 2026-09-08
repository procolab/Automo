import csv
import json

file_name = "employees.csv"
print("---------------------------------------------")
### 1. Write (Create CSV File and write some data.)

print("1. Write (Create CSV File and write some data.)")
data = [
    ["ID", "Name", "Age", "Salary"],
    [101, "Himanshu", 30, 987],
    [102, "Rahul", 28, 928],
    [103, "Amit", 32, 1080]
]
with open(file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV File 'employees.csv' Created Successfully")

print("---------------------------------------------")
### 2. Read CSV file.

print("2. Read CSV file.")
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 3. Add New Record in CSV file.

print("3. Add New Record in CSV file. File O/P")
new_record = [104, "Sneha", 27, 550]
with open(file_name, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(new_record)

print("Record Added Successfully")
# To check O/P
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 4. Load CSV file into memory.

print("4. Load CSV file into memory.")
with open(file_name, "r") as file:
    rows = list(csv.reader(file))

# To check O/P
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 5. Search record in CSV file.

print("5. Search record in CSV file. For id 102.")
search_id = "102"
for row in rows[1:]:
    if row[0] == search_id:
        print("Record Found:", row)

# To check O/P
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 6. Update record in CSV file.

print("6. Update record in CSV file.")
print("For id 102 Name 'Rahul'->'Rahul Sharma' & Age '28'->'29' & Salary '928'-> '48000'")
for row in rows[1:]:
    if row[0] == "102":
        row[1] = "Rahul Sharma"
        row[2] = "29"
        row[3] = "480"

with open(file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Record Updated Successfully")

# To check O/P
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 7. Delete record from CSV file.

print("7. Delete record from CSV file. For id 103.")
rows = [row for row in rows if row[0] != "103"]
with open(file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Record Deleted Successfully")

# To check O/P
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 8. Sort record by salary.

print("8. Sort record by salary.")
header = rows[0]
records = rows[1:]
records.sort(key=lambda x: int(x[3]))  # Ascending
print(header)
for record in records:
    print(record)

print("---------------------------------------------")
### 9. Save the sorted data in CSV file.

print("9. Save the sorted data in CSV file.")
with open(file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(records)

# To check O/P
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("---------------------------------------------")
### 10. CSV data convert in JSON data.

print("10. CSV data convert in JSON data.")
print("CSV file data.")
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("\nJSON data O/P.")
with open(file_name, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    # json.dumps() turns the Python list into a JSON string
    json_string = json.dumps(list(reader), indent=4)

print(json_string)

print("---------------------------------------------")
### 11. Final CSV file data.

print("11. Final CSV file data.")
with open(file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
print("---------------------------------------------")
