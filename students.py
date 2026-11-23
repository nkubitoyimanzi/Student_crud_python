from database import get_connection, initialize_database


def create_student():
    student_name = input("Enter name: ")
    student_age = input("Enter age: ")

    if not student_name:
        print("Name cant be empty! ")
        return

    if not student_age.isdigit() or int(student_age) <= 0:
        print("Age can't be less than 0")
        return

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO students (name, age ) VALUES (?, ?)", (student_name, int(student_age)))

        student_id = cursor.lastrowid
    print(f"The student {student_name} is added with id {student_id}")


def display_students():
    with get_connection() as connection:
        students = connection.execute(
            "SELECT * FROM students ORDER BY id "
        ).fetchall()

    if not students:
        print("No student found")
        return

    print("\n STUDENTS")

    for student in students:
        print(
            f"Id: {student['id']}|"
            f"Name: {student['name']}|"
            f"Age: {student['age']}"
        )


def find_student(student_id):
    with get_connection() as connection:
        student = connection.execute(
            "SELECT * FROM students where id = ?", (student_id,)).fetchone()

    return student


def update_student():

    student_id = input("Enter the id of student to update").strip()
    if not student_id.isdigit() or int(student_id) <= 0:
        print("Student id must be a positive value")
        return

    student = find_student(int(student_id))

    if student is None:
        print("Student not found")

        return

    print(f"Current name: {student['name']}")
    print(f"Current age: {student['age']}")

    new_name = input("Enter new name (press Enter to keep current): ").strip()
    new_age = input("Enter new age (press Enter to keep current): ").strip()

    if new_name == "" and new_age == "":
        print("No changes  made ")
        return

    if new_name == "":
        new_name = student["name"]

    if new_age == "":
        new_age = student["age"]
    elif not new_age.isdigit() or int(new_age) <= 0:
        print("Age must be a positive value")
        return
    else:
        new_age = int(new_age)

    with get_connection() as connection:
        connection.execute("UPDATE students SET name = ?, age = ? WHERE id = ?",
                           (new_name, new_age, int(student_id)))

    print("Updated successfully")


def delete_student():

    student_id = input("Enter student id to delete").strip()

    if not student_id.isdigit() or int(student_id) <= 0:
        print(" Id should be a positive value!")
        return
    student = find_student(int(student_id))

    if student is None:
        print("Student not found.")
        return

    print(f"Student selected: {student['name']}")

    with get_connection() as connection:
        connection.execute(
            "DELETE FROM students WHERE id = ?",
            (int(student_id),)
        )

    print(f"Student '{student['name']}' deleted successfully.")
