from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "mysql+pymysql://root:146002233_Tt@localhost/learning"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = 'Student'
    Student_ID = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(50))
    Last_Name = Column(String(50))
    Record_Book_ID = Column(String(20))
    Course = Column(Integer)
    grades = relationship("Grade", back_populates="student", cascade="all, delete")

class Discipline(Base):
    __tablename__ = 'Discipline'
    Discipline_ID = Column(Integer, primary_key=True, autoincrement=True)
    Discipline_Name = Column(String(100), nullable=False)

class Grade(Base):
    __tablename__ = 'Grade'
    Grade_ID = Column(Integer, primary_key=True, autoincrement=True)
    Student_ID = Column(Integer, ForeignKey('Student.Student_ID', ondelete="CASCADE"))
    Discipline_ID = Column(Integer, ForeignKey('Discipline.Discipline_ID', ondelete="CASCADE"))
    Grade_Value = Column(Integer)

    student = relationship("Student", back_populates="grades")
    discipline = relationship("Discipline")

Base.metadata.create_all(engine)

def add_student(first_name, last_name, record_book_id, course, grades):
    new_student = Student(First_Name=first_name, Last_Name=last_name, Record_Book_ID=record_book_id, Course=course)
    session.add(new_student)
    session.commit()

    for discipline_id, grade_value in grades:
        discipline = session.query(Discipline).filter_by(Discipline_ID=discipline_id).first()
        if not discipline:
            print(f"❌ Дисципліна з ID {discipline_id} не знайдена! Оцінка не додана.")
            continue
        new_grade = Grade(Student_ID=new_student.Student_ID, Discipline_ID=discipline_id, Grade_Value=grade_value)
        session.add(new_grade)

    session.commit()
    print(f"✅ Додано студента: {first_name} {last_name} разом із оцінками")

def get_student(student_id):
    student = session.query(Student).filter_by(Student_ID=student_id).first()
    if student:
        print(f"🎓 Студент: {student.First_Name} {student.Last_Name}, Курс: {student.Course}")
        for grade in student.grades:
            print(f"   {grade.discipline.Discipline_Name}: {grade.Grade_Value}")
    else:
        print("❌ Студента не знайдено!")

def update_student(student_id, new_first_name=None, new_last_name=None, new_course=None):
    student = session.query(Student).filter_by(Student_ID=student_id).first()
    if student:
        if new_first_name:
            student.First_Name = new_first_name
        if new_last_name:
            student.Last_Name = new_last_name
        if new_course:
            student.Course = new_course
        session.commit()
        print("✅ Студента оновлено!")
    else:
        print("❌ Студента не знайдено!")

def delete_student(student_id):
    student = session.query(Student).filter_by(Student_ID=student_id).first()
    if student:
        session.delete(student)
        session.commit()
        print("✅ Студента видалено разом із його оцінками!")
    else:
        print("❌ Студента не знайдено!")

def get_all_students():
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.Student_ID}, {student.First_Name} {student.Last_Name}, Курс: {student.Course}")


def add_discipline(name):
    new_discipline = Discipline(Discipline_Name=name)
    session.add(new_discipline)
    session.commit()
    print(f"✅ Додано дисципліну: {name}")

def get_all_disciplines():
    disciplines = session.query(Discipline).all()
    for discipline in disciplines:
        print(f"ID: {discipline.Discipline_ID}, Назва: {discipline.Discipline_Name}")

def update_discipline(discipline_id, new_name):
    discipline = session.query(Discipline).filter_by(Discipline_ID=discipline_id).first()
    if discipline:
        discipline.Discipline_Name = new_name
        session.commit()
        print("✅ Дисципліну оновлено!")
    else:
        print("❌ Дисципліну не знайдено!")

def delete_discipline(discipline_id):
    discipline = session.query(Discipline).filter_by(Discipline_ID=discipline_id).first()
    if discipline:
        session.delete(discipline)
        session.commit()
        print("✅ Дисципліну видалено!")
    else:
        print("❌ Дисципліну не знайдено!")

def update_grade(student_id, discipline_id, new_grade):
    grade = session.query(Grade).filter_by(Student_ID=student_id, Discipline_ID=discipline_id).first()
    if grade:
        grade.Grade_Value = new_grade
        session.commit()
        print("✅ Оцінку оновлено!")
    else:
        print("❌ Оцінка не знайдена!")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Помилка! Введіть команду (наприклад, get_student 1)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "get_student":
        student_id = int(sys.argv[2])
        get_student(student_id)

    elif command == "add_student":
        first_name = sys.argv[2]
        last_name = sys.argv[3]
        record_book_id = sys.argv[4]
        course = int(sys.argv[5])
        grades = [tuple(map(int, g.split(":"))) for g in sys.argv[6].split(",")]
        add_student(first_name, last_name, record_book_id, course, grades)

    elif command == "add_discipline":
        name = sys.argv[2]
        add_discipline(name)

    elif command == "get_all_disciplines":
        get_all_disciplines()

    elif command == "update_discipline":
        discipline_id = int(sys.argv[2])
        new_name = sys.argv[3]
        update_discipline(discipline_id, new_name)

    elif command == "delete_discipline":
        discipline_id = int(sys.argv[2])
        delete_discipline(discipline_id)

    elif command == "get_all_students":
        get_all_students()

    elif command == "update_grade":
        student_id = int(sys.argv[2])
        discipline_id = int(sys.argv[3])
        new_grade = int(sys.argv[4])
        update_grade(student_id, discipline_id, new_grade)

    elif command == "update_student":
        student_id = int(sys.argv[2])
        new_first_name = sys.argv[3] if sys.argv[3] != "None" else None
        new_last_name = sys.argv[4] if sys.argv[4] != "None" else None
        new_course = int(sys.argv[5]) if sys.argv[5] != "None" else None
        update_student(student_id, new_first_name, new_last_name, new_course)

    elif command == "delete_student":
        student_id = int(sys.argv[2])
        delete_student(student_id)

    else:
        print("❌ Невідома команда! Доступні команди:")
        print("   get_student, add_student, update_student, delete_student")
        print("   get_all_students, add_discipline, get_all_disciplines")
        print("   update_discipline, delete_discipline, update_grade")
