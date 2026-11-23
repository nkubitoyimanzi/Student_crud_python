from database import initialize_database
from students import (
    create_student,
    display_students,
    update_student,
    delete_student,
)


def main():
    initialize_database() 

    while True:
        print("\n1. Create  2. display  3. Update  4. Delete  5. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            create_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Exit!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()