from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "Student"

    Student_ID = Column(Integer, primary_key=True)
    First_Name = Column(String(50), nullable=False)
    Last_Name = Column(String(50), nullable=False)
    Record_Book_ID = Column(String(20), nullable=False)
    Course = Column(Integer, nullable=False)

    grades = relationship("Grade", back_populates="student")


class Discipline(Base):
    __tablename__ = "Discipline"

    Discipline_ID = Column(Integer, primary_key=True)
    Discipline_Name = Column(String(100), nullable=False)

    grades = relationship("Grade", back_populates="discipline")


class Grade(Base):
    __tablename__ = "Grade"

    Grade_ID = Column(Integer, primary_key=True)
    Student_ID = Column(Integer, ForeignKey("Student.Student_ID"))
    Discipline_ID = Column(Integer, ForeignKey("Discipline.Discipline_ID"))
    Grade_Value = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="grades")
    discipline = relationship("Discipline", back_populates="grades")
