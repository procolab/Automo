from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

file_name = "employees.csv"

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

# ==============================
# Helper Functions
# ==============================

def read_data():
    with open(file_name, "r") as file:
        return list(csv.DictReader(file))


def write_data(data):
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["ID", "Name", "Age", "Contact"]
        )
        writer.writeheader()
        writer.writerows(data)


# ==========================================
# 1. GET ALL STUDENTS
# ==========================================
@app.route("/students", methods=["GET"])
def get_all_students():
    return jsonify(read_data())


# ==========================================
# 2. GET STUDENT BY ROLLNO(ID)
# ==========================================
@app.route("/students/<id>", methods=["GET"])
def get_student(id):

    students = read_data()

    for student in students:
        if student["ID"] == id:
            return jsonify(student)

    return jsonify({"message": "Student not found"}), 404


# ==========================================
# 3. POST CREATE NEW STUDENT
# ==========================================
@app.route("/students", methods=["POST"])
def add_student():

    new_student = request.json

    students = read_data()

    for student in students:
        if student["ID"] == str(new_student["ID"]):
            return jsonify(
                {"message": "Student already exists"}
            ), 400

    students.append({
        "ID": str(new_student["ID"]),
        "Name": new_student["Name"],
        "Age": str(new_student["Age"]),
        "Contact": new_student["Contact"]
    })

    write_data(students)

    return jsonify({
        "message": "Student Added Successfully"
    }), 201


# ==========================================
# 4. PUT UPDATE COMPLETE RECORD
# ==========================================
@app.route("/students/<id>", methods=["PUT"])
def update_student(id):

    updated_data = request.json

    students = read_data()

    for student in students:

        if student["ID"] == id:

            student["Name"] = updated_data["Name"]
            student["Age"] = str(updated_data["Age"])
            student["Contact"] = updated_data["Contact"]

            write_data(students)

            return jsonify({
                "message": "Student Updated Successfully"
            })

    return jsonify({"message": "Student not found"}), 404


# ==========================================
# 5. PATCH PARTIAL UPDATE
# ==========================================
@app.route("/students/<id>", methods=["PATCH"])
def patch_student(id):

    patch_data = request.json

    students = read_data()

    for student in students:

        if student["ID"] == id:

            if "Name" in patch_data:
                student["Name"] = patch_data["Name"]

            if "Age" in patch_data:
                student["Age"] = str(patch_data["Age"])

            if "Contact" in patch_data:
                student["Contact"] = patch_data["Contact"]

            write_data(students)

            return jsonify({
                "message": "Student Partially Updated"
            })

    return jsonify({"message": "Student not found"}), 404


# ==========================================
# 6. DELETE STUDENT
# ==========================================
@app.route("/students/<id>", methods=["DELETE"])
def delete_student(id):

    students = read_data()

    new_students = [
        student
        for student in students
        if student["ID"] != id
    ]

    if len(new_students) == len(students):
        return jsonify({
            "message": "Student not found"
        }), 404

    write_data(new_students)

    return jsonify({
        "message": "Student Deleted Successfully"
    })


# ==========================================
# Run Application
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
