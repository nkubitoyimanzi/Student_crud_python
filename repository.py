from database import get_connection


def create_student(name, age):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO students (name,age) VALUES (?,?)", (name, age))
        return cursor.lastrowid


def get_students():
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM students ORDER BY id ").fetchall()


def get_one_student(student_id):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
            ).fetchone()

def get_students_page(page, per_page, search=""):
    offset = (page - 1) * per_page
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM students WHERE name LIKE ? ORDER BY id LIMIT ? OFFSET ?",
            ("%" + search + "%", per_page, offset),
        ).fetchall()

def update_student(student_id, name, age):
    with get_connection() as connection:
        connection.execute(
            "UPDATE students SET name = ?, age = ? where id = ?", (name, age, student_id),)


def delete_student(student_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM students WHERE id = ?", (student_id,))


def student_count(search=""):
    with get_connection() as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM students WHERE name LIKE ?",
            ("%" + search + "%",),
        ).fetchone()[0]        
