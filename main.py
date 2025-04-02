from database import SessionLocal
import crud

db = SessionLocal()

new_student = crud.create_student(db, "Іван", "Петренко", "RB010", 3)
print(f"Додано студента: {new_student.First_Name} {new_student.Last_Name}")

students = crud.get_students(db)
print("Список студентів:")
for s in students:
    print(f"ID: {s.Student_ID}, Ім'я: {s.First_Name} {s.Last_Name}")

db.close()
