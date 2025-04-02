from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from database import Student, Discipline, Grade, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/students')
def students():
    return render_template('student_form.html')

@app.route('/disciplines')
def disciplines():
    return render_template('discipline_form.html')

@app.route('/grades')
def grades():
    return render_template('grade_form.html')

@app.route('/students/index')
def students_index():
    students = session.query(Student).all()
    return render_template('students_index.html', students=students)

@app.route('/disciplines/index')
def disciplines_index():
    disciplines = session.query(Discipline).all()
    return render_template('disciplines_index.html', disciplines=disciplines)

@app.route('/grades/index')
def grades_index():
    grades = session.query(Grade).all()
    return render_template('grades_index.html', grades=grades)

@app.route('/students/show/<int:id>')
def students_show(id):
    student = session.query(Student).get(id)
    return render_template('students_show.html', student=student)

@app.route('/disciplines/show/<int:id>')
def disciplines_show(id):
    discipline = session.query(Discipline).get(id)
    return render_template('disciplines_show.html', discipline=discipline)

@app.route('/grades/show/<int:id>')
def grades_show(id):
    grade = session.query(Grade).get(id)
    return render_template('grades_show.html', grade=grade)

@app.route('/manage_students', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_students():
    if request.method == 'GET':
        students = session.query(Student).all()
        return jsonify([s.to_dict() for s in students])
    elif request.method == 'POST':
        new_student = Student(
            First_Name=request.form['First_Name'],
            Last_Name=request.form['Last_Name'],
            Course=request.form['Course']
        )
        session.add(new_student)
        session.commit()
        flash("Студент успішно доданий!", "success")
        return redirect(url_for('students'))
    elif request.method == 'PUT':
        data = request.get_json()
        student = session.query(Student).get(data['id'])
        if student:
            student.First_Name = data['First_Name']
            student.Last_Name = data['Last_Name']
            student.Course = data['Course']
            session.commit()
            flash("Студент оновлений успішно!", "success")
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        data = request.get_json()
        student = session.query(Student).get(data['id'])
        if student:
            session.delete(student)
            session.commit()
            flash("Студент видалений успішно!", "success")
        return jsonify({'status': 'deleted'})

@app.route('/manage_disciplines', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_disciplines():
    if request.method == 'GET':
        disciplines = session.query(Discipline).all()
        return jsonify([d.to_dict() for d in disciplines])
    elif request.method == 'POST':
        new_discipline = Discipline(Discipline_Name=request.form['Discipline_Name'])
        session.add(new_discipline)
        session.commit()
        flash("Дисципліна успішно додана!", "success")
        return redirect(url_for('disciplines'))
    elif request.method == 'PUT':
        data = request.get_json()
        discipline = session.query(Discipline).get(data['id'])
        if discipline:
            discipline.Discipline_Name = data['Discipline_Name']
            session.commit()
            flash("Дисципліна оновлена успішно!", "success")
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        data = request.get_json()
        discipline = session.query(Discipline).get(data['id'])
        if discipline:
            session.delete(discipline)
            session.commit()
            flash("Дисципліна видалена успішно!", "success")
        return jsonify({'status': 'deleted'})

@app.route('/manage_grades', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_grades():
    if request.method == 'GET':
        grades = session.query(Grade).all()
        return jsonify([g.to_dict() for g in grades])
    elif request.method == 'POST':
        new_grade = Grade(
            Student_ID=request.form['Student_ID'],
            Discipline_ID=request.form['Discipline_ID'],
            Grade_Value=request.form['Grade_Value']
        )
        session.add(new_grade)
        session.commit()
        flash("Оцінка успішно додана!", "success")
        return redirect(url_for('grades'))
    elif request.method == 'PUT':
        data = request.get_json()
        grade = session.query(Grade).get(data['id'])
        if grade:
            grade.Student_ID = data['Student_ID']
            grade.Discipline_ID = data['Discipline_ID']
            grade.Grade_Value = data['Grade_Value']
            session.commit()
            flash("Оцінка оновлена успішно!", "success")
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        data = request.get_json()
        grade = session.query(Grade).get(data['id'])
        if grade:
            session.delete(grade)
            session.commit()
            flash("Оцінка видалена успішно!", "success")
        return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(debug=False)
