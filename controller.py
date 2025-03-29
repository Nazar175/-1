from flask import Flask, request, jsonify
from database import Student, Discipline, Grade, session

app = Flask(__name__)


@app.route('/students', methods=['GET'])
def get_students():
    students = session.query(Student).all()
    return jsonify([{"id": s.Student_ID, "first_name": s.First_Name, "last_name": s.Last_Name, "course": s.Course} for s in students])

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = session.query(Student).get(student_id)
    if student:
        return jsonify({"id": student.Student_ID, "first_name": student.First_Name, "last_name": student.Last_Name, "course": student.Course})
    return {"error": "Student not found"}, 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(**data)
    session.add(new_student)
    session.commit()
    return {"message": "Student added!"}, 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = session.query(Student).get(student_id)
    if not student:
        return {"error": "Student not found"}, 404
    data = request.json
    for key, value in data.items():
        setattr(student, key, value)
    session.commit()
    return {"message": "Student updated"}

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = session.query(Student).get(student_id)
    if not student:
        return {"error": "Student not found"}, 404
    session.delete(student)
    session.commit()
    return {"message": "Student deleted"}


@app.route('/disciplines', methods=['GET'])
def get_disciplines():
    disciplines = session.query(Discipline).all()
    return jsonify([{"id": d.Discipline_ID, "name": d.Discipline_Name} for d in disciplines])

@app.route('/disciplines', methods=['POST'])
def add_discipline():
    data = request.json
    new_discipline = Discipline(**data)
    session.add(new_discipline)
    session.commit()
    return {"message": "Discipline added!"}, 201

@app.route('/disciplines/<int:discipline_id>', methods=['PUT'])
def update_discipline(discipline_id):
    discipline = session.query(Discipline).get(discipline_id)
    if not discipline:
        return {"error": "Discipline not found"}, 404
    data = request.json
    discipline.Discipline_Name = data.get("Discipline_Name", discipline.Discipline_Name)
    session.commit()
    return {"message": "Discipline updated"}

@app.route('/disciplines/<int:discipline_id>', methods=['DELETE'])
def delete_discipline(discipline_id):
    discipline = session.query(Discipline).get(discipline_id)
    if not discipline:
        return {"error": "Discipline not found"}, 404
    session.delete(discipline)
    session.commit()
    return {"message": "Discipline deleted"}


@app.route('/grades/<int:student_id>', methods=['GET'])
def get_grades(student_id):
    grades = session.query(Grade).filter_by(Student_ID=student_id).all()
    return jsonify([{"id": g.Grade_ID, "discipline": g.Discipline_ID, "grade": g.Grade_Value} for g in grades])

@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.json
    new_grade = Grade(**data)
    session.add(new_grade)
    session.commit()
    return {"message": "Grade added!"}, 201

@app.route('/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    grade = session.query(Grade).get(grade_id)
    if not grade:
        return {"error": "Grade not found"}, 404
    data = request.json
    grade.Grade_Value = data.get("Grade_Value", grade.Grade_Value)
    session.commit()
    return {"message": "Grade updated"}

@app.route('/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    grade = session.query(Grade).get(grade_id)
    if not grade:
        return {"error": "Grade not found"}, 404
    session.delete(grade)
    session.commit()
    return {"message": "Grade deleted"}


if __name__ == "__main__":
    app.run(debug=False)
