from database import initialize_database
from repository import create_student

initialize_database()

for i in range(1, 13):
    create_student("Student " + str(i), 18 + i)

print("Added 12 students")
