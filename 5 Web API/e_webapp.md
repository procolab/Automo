# Flask CSV CRUD API

A Lightweight RESTful JSON API built with Python and Flask. This program provides endpoints to perform CRUD (Create, Read, Update, Delete) operations on a local `students.csv` file using standard HTTP methods.

---

## File Structure

```text
.
app.py           # Main Flask application with API endpoints
students.csv     # CSV file storing record data
README.md        # Documentation
```

---

## CSV Data Format (`students.csv`)

The data is persisted in a CSV file structured with the following headers:

```csv
rollno,name,age,contact
101,John Doe,20,1234567890
102,Jane Smith,22,0987654321
```

---

## Setup & Installation

1. **Clone the repository** or create the files locally.
2. **Install Flask**:
   ```bash
   pip install flask
   ```
3. **Run the application**:
   ```bash
   python app.py
   ```
   The API will start at `http://127.0.0.1:5000`.

---

## » Python Source Code (`app.py`)

```python
import csv
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
CSV_FILE = 'students.csv'
HEADERS = ['rollno', 'name', 'age', 'contact']

def initialize_csv():
    """Create CSV file with headers if it does not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)

def read_csv():
    """Read data from CSV into a list of dictionaries."""
    students = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    return students

def write_csv(students):
    """Write a list of dictionaries back to the CSV file."""
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(students)

@app.route('/students', methods=['GET'])
def get_all_students():
    """GET: Retrieve all student records."""
    students = read_csv()
    return jsonify({"success": True, "data": students}), 200

@app.route('/students/<rollno>', methods=['GET'])
def get_student(rollno):
    """GET: Retrieve a single student by rollno."""
    students = read_csv()
    student = next((s for s in students if s['rollno'] == str(rollno)), None)
    if student:
        return jsonify({"success": True, "data": student}), 200
    return jsonify({"success": False, "message": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    """POST: Create a new student record."""
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in HEADERS):
        return jsonify({"success": False, "message": "Missing required fields: rollno, name, age, contact"}), 400

    students = read_csv()
    # Check if rollno already exists
    if any(s['rollno'] == str(data['rollno']) for s in students):
        return jsonify({"success": False, "message": "Student with this rollno already exists"}), 400

    new_student = {
        "rollno": str(data['rollno']),
        "name": str(data['name']),
        "age": str(data['age']),
        "contact": str(data['contact'])
    }
    students.append(new_student)
    write_csv(students)
    return jsonify({"success": True, "message": "Student added successfully", "data": new_student}), 201

@app.route('/students/<rollno>', methods=['PUT'])
def update_student(rollno):
    """PUT: Update an existing student completely or partially."""
    data = request.get_json()
    students = read_csv()
    
    student = next((s for s in students if s['rollno'] == str(rollno)), None)
    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404

    # Update student attributes
    student['name'] = str(data.get('name', student['name']))
    student['age'] = str(data.get('age', student['age']))
    student['contact'] = str(data.get('contact', student['contact']))

    write_csv(students)
    return jsonify({"success": True, "message": "Student updated successfully", "data": student}), 200

@app.route('/students/<rollno>', methods=['DELETE'])
def delete_student(rollno):
    """DELETE: Remove a student record by rollno."""
    students = read_csv()
    filtered_students = [s for s in students if s['rollno'] != str(rollno)]

    if len(students) == len(filtered_students):
        return jsonify({"success": False, "message": "Student not found"}), 404

    write_csv(filtered_students)
    return jsonify({"success": True, "message": "Student deleted successfully"}), 200

if __name__ == '__main__':
    initialize_csv()
    app.run(debug=True)
```

---

## API Reference & Endpoints

| Method | Endpoint | Description | Request Body (JSON) |
| :--- | :--- | :--- | :--- |
| **GET** | `/students` | Get all student records | None |
| **GET** | `/students/<rollno>` | Get a student by Roll No | None |
| **POST** | `/students` | Add a new student record | `{"rollno": "103", "name": "Alice", "age": "21", "contact": "55512345"}` |
| **PUT** | `/students/<rollno>` | Update an existing student | `{"name": "Alice Green", "age": "22", "contact": "55599999"}` |
| **DELETE**| `/students/<rollno>` | Delete a student by Roll No | None |

---

## Testing with cURL

**1. Create a Student (POST)**
```bash
curl -X POST http://127.0.0.1:5000/students \
     -H "Content-Type: application/json" \
     -d '{"rollno": "101", "name": "John Doe", "age": "20", "contact": "1234567890"}'
```

**2. Get All Students (GET)**
```bash
curl http://127.0.0.1:5000/students
```

**3. Get Single Student (GET)**
```bash
curl http://127.0.0.1:5000/students/101
```

**4. Update a Student (PUT)**
```bash
curl -X PUT http://127.0.0.1:5000/students/101 \
     -H "Content-Type: application/json" \
     -d '{"name": "John Smith", "age": "21", "contact": "9998887770"}'
```

**5. Delete a Student (DELETE)**
```bash
curl -X DELETE http://127.0.0.1:5000/students/101
```
