import json

### JSON Data in String (All Data Types)

json_str = '''
{
    "name": "Himanshu",
    "age": 30,
    "salary": 90.75,
    "is_employee": true,
    "manager": null,
    "skills": ["Python", "SQL", "Azure"],
    "address": {
        "city": "Noida",
        "state": "UP"
    }
}
'''

### JSON -> Python Dictionary
data = json.loads(json_str)

print("------ 1. ORIGINAL DATA ------")
print(json.dumps(data, indent=4))

### ACCESS OPERATIONS
print("\n------ 2. ACCESS ------")

### Direct Access
print("Name key:", data["name"])

## Safe Access
print("Age key:", data.get("age"))
print("Mobile key:", data.get("mobile", "Not Found"))

## Nested Access
print("City key of 'address':", data["address"]["city"])

## List Access
print("First Skill key 0th:", data["skills"][0])

### CHECK OPERATIONS
print("\n------ 3. CHECK ------")

print("name exists ?:", "name" in data)
print("department exists ?:", "department" in data)

print("Python skill exists ?:", "Python" in data["skills"])

print("Type of data ?:", type(data).__name__)
print("Type of skills ?:", type(data["skills"]).__name__)

### ADD OPERATIONS
print("\n------ 4. ADD ------")

## Add new key
data["department"] = "IT"
print("Added new key 'department' = 'IT' in JSON")

## Add multiple values
data.update({
    "country": "India",
    "experience": 8
})
print("Added new key 'country' = 'India' & 'experience' = '8' in JSON")

## Add item to list
data["skills"].append("Power BI")
print("Added new key in List 'skills' 3rd value 'Power BI' in JSON")

print("After add new 'key':'value' in JSON Date:")
print(json.dumps(data, indent=4))

### UPDATE OPERATIONS
print("\n------ 5. UPDATE ------")

# Update key
print("Updating 'age' value 30->31")
data["age"] = 31

# Update nested key
print("Updating 'address' nested key 'city' value Noida->Delhi")
data["address"]["city"] = "Delhi"

# Update list value
print("Updating 'skills' value 1st place SQL->MySQL")
data["skills"][1] = "MySQL"

print(json.dumps(data, indent=4))

### REMOVE OPERATIONS
print("\n------ 6. REMOVE ------")

# Remove key using pop
removed_age = data.pop("age")
print("Removed age:", removed_age)

# Remove key using del
del data["salary"]
print("Removed 'salary' key")

# Remove list item
data["skills"].remove("Azure")
print("Removed from 'skills' List value 'Azure'")

# Remove last item
data["skills"].pop()
print("Removed from 'skills' List last value")

print("After remove some key and some value")
print(json.dumps(data, indent=4))

### LOOP OPERATIONS
print("\n------ 7. LOOP ------")

print("Test loop operation:")
for key, value in data.items():
    print(f"{key} = {value}")

### JSON CONVERSION
print("\n------ 8. JSON STRING ------")

print("Now Dictionary data type convert in JSON:")
json_output = json.dumps(data, indent=4)
print(json_output)

### FINAL RESULT
print("\n------ 9. FINAL DATA ------")
print(json.dumps(data, indent=4))
