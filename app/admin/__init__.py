from app import app, session, render_template, redirect, request, bcrypt
from app.models import *


@app.route('/admin/', methods=["GET"])
def administrator():
    if 'user' in session:
        if session['user']['adminStatus'] == True:
            all_courses = [course.to_json() for course in Course.query.all()]
            all_students = [student.to_json() for student in Student.query.all()]
            all_lecturers = [lecturer.to_json() for lecturer in Lecturer.query.all()]
            all_rooms = [room.to_json() for room in Classroom.query.all()]
            all_tables = [table.json() for table in TimeTable.query.all()]
            return render_template('admin.html', courses=all_courses, lecturers=all_lecturers, students=all_students, rooms=all_rooms, tables=all_tables)
        return redirect(f"/user/{session['user']['id']}")
    return redirect('/auth/login')

@app.route('/admin/addcourse', methods=["POST"])
def handle_courses():
    if 'user' in session:
        if session['user']['adminStatus'] == True:
            if(request.form.get('name') and request.form.get('number') and request.form.get('desc') and request.form.get('level') and request.form.get('credit')):
                new_course = Course(name=request.form.get('name'), number=request.form.get('number'), description=request.form.get('desc'), level=request.form.get('level'), credit=request.form.get('credit'))
                db.session.add(new_course)
                db.session.commit()
                return redirect('/admin/')
            return redirect('/admin/')
        return redirect(f"/user/{session['user']['id']}")
    return redirect('/admin/login')

@app.route('/admin/addstudents', methods=["POST"])
def handle_users():
    if 'user' in session:
        if session['user']['adminStatus'] == True:
            if(request.form.get('firstname') and request.form.get('lastname') and request.form.get('email') and request.form.get('phone') and request.form.get('year')):
                password = bcrypt.hashpw(u'abcd1234'.encode('utf-8'), bcrypt.gensalt(10))
                new_user = User(email=request.form.get('email'), password=password, firstname=request.form.get('firstname'), surname=request.form.get('lastname'), maidname=request.form.get('othername'), phone=request.form.get('phone'), usertype='S', isAdmin=False)
                db.session.add(new_user)
                db.session.flush()
                new_student = Student(usertype='S', user=new_user.id, year=request.form.get('year'), department=request.form.get('department'))
                db.session.add(new_student)
                db.session.commit()
                return redirect('/admin/')
            return redirect('/admin/')
        return redirect(f"/user/{session['user']['id']}")
    return redirect('/auth/login')

@app.route('/admin/addlecturer', methods=["POST"])
def handle_lecture():
    if 'user' in session:
        if session['user']['adminStatus'] == True:
            isadmin = False
            if request.form.get('isadmin'):
                isadmin = True
            if(request.form.get('firstname') and request.form.get('lastname') and request.form.get('email') and request.form.get('phone') and request.form.get('office')):
                password = bcrypt.hashpw(u'abcd1234'.encode('utf-8'), bcrypt.gensalt(10))
                new_user = User(email=request.form.get('email'), password=password, firstname=request.form.get('firstname'), surname=request.form.get('lastname'), maidname=request.form.get('othername'), phone=request.form.get('phone'), usertype='L', isAdmin=isadmin)
                db.session.add(new_user)
                db.session.flush()
                new_lecturer = Lecturer(usertype='L', user=new_user.id, office=request.form.get('office'))
                db.session.add(new_lecturer)
                db.session.commit()
                return redirect('/admin/')
            return redirect('/admin/')
        return redirect(f"/user/{session['user']['id']}")
    return redirect('/auth/login')


@app.route('/<section>/delete/<id>', methods=['POST', 'DELETE'])
def delete_content(section, id):
    if 'user' in session:
        if section in ['student', 'lecturer']:
            if section == 'lecturer' and session['user']['id'] == Lecturer.query.filter_by(id=id).first().user:
                return redirect('/admin/')
            item = eval(section.capitalize()).query.filter_by(id=id)
            item_user = User.query.filter_by(id=item.first().user).delete()
            item.delete()
            db.session.commit()
            return redirect('/admin/')
        if section == 'course':
            item = Course.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect('/admin/')
    return redirect('/auth/login')