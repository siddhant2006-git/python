import os
import json

Date_file = "student_data.json"
subjects = ["english", "hindi", "math", "science"]


def load_data():
    if os.path.exists(Date_file):
        with open(Date_file, "r") as file:
            return json.load(file)
    return []


def save_data(data):
    with open(Date_file, "w") as file:
        json.dump(data, file, indent=4)


def calculator(marks):
    total_marks = sum(marks.values())
    max_marks = len(marks) * 100
    percentage = (total_marks / max_marks) * 100

    if percentage >= 90:
        grade = "A"
    elif percentage >= 80:
        grade = "B"
    elif percentage >= 70:
        grade = "C"
    elif percentage >= 60:
        grade = "D"
    else:
        grade = "E"

    return round(percentage, 2), grade


def addstudent():
    print("\n--- Add New Student ---")

    name = input("enter the name = ").strip()
    roll_no = input("enter the roll no = ").strip()

    marks = {}
    print("enter the marks out of 100")

    for subject in subjects:
        marks[subject] = int(input(f"enter the value of {subject}: "))

    percentage, grade = calculator(marks)

    student = {
        "name": name,
        "roll_no": roll_no,
        "marks": marks,
        "percentage": percentage,
        "grade": grade,
    }

    data = load_data()
    data.append(student)
    save_data(data)

    print("Student added successfully!")


addstudent()


