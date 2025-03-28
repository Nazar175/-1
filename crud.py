from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:146002233_Tt@localhost/learning"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

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
    Discipline_Name = Column(String(100))

class Grade(Base):
    __tablename__ = 'Grade'
    Grade_ID = Column(Integer, primary_key=True, autoincrement=True)
    Student_ID = Column(Integer, ForeignKey('Student.Student_ID', ondelete='CASCADE'))
    Discipline_ID = Column(Integer, ForeignKey('Discipline.Discipline_ID', ondelete='CASCADE'))
    Grade_Value = Column(Integer)
    student = relationship("Student", back_populates="grades")

def add_student_with_grades(first_name, last_name, record_book_id, course, grades):
    student = Student(First_Name=first_name, Last_Name=last_name, Record_Book_ID=record_book_id, Course=course)
    session.add(student)
    session.commit()
    
    for discipline_id, grade_value in grades.items():
        grade = Grade(Student_ID=student.Student_ID, Discipline_ID=discipline_id, Grade_Value=grade_value)
        session.add(grade)
    session.commit()
    print(f"Додано студента: {first_name} {last_name} разом з оцінками")

def update_student(student_id, first_name=None, last_name=None, record_book_id=None, course=None):
    student = session.query(Student).filter_by(Student_ID=student_id).first()
    if not student:
        print("Студента не знайдено")
        return
    if first_name:
        student.First_Name = first_name
    if last_name:
        student.Last_Name = last_name
    if record_book_id:
        student.Record_Book_ID = record_book_id
    if course:
        student.Course = course
    session.commit()
    print(f"Оновлено дані студента ID {student_id}")

def delete_student(student_id):
    student = session.query(Student).filter_by(Student_ID=student_id).first()
    if not student:
        print("Студента не знайдено")
        return
    session.delete(student)
    session.commit()
    print(f"Студента ID {student_id} видалено")

def get_students():
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.Student_ID}, Ім'я: {student.First_Name} {student.Last_Name}, Курс: {student.Course}")

if __name__ == "__main__":
    add_student_with_grades("Іван", "Петренко", "RB010", 3, {1: 5, 2: 4})
    update_student(1, first_name="Олег")
    get_students()
    delete_student(1)
