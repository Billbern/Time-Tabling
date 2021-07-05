from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(96), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(), unique=False)
    firstname = db.Column(db.String(200), nullable=False)
    maidname = db.Column(db.String(200))
    surname = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    usertype = db.Column(db.String(1), nullable=False)
    isAdmin = db.Column(db.Boolean(), default=False)
    __table_args__ = (db.CheckConstraint(usertype.in_(['L', 'S'])), )

    def fullname(self):
        return f"{self.firstname} {self.surname}"

    def to_json(self):
        return {"id": self.id, "email": self.email, "First Name": self.firstname, "Last name": self.surname, 'Phone': self.phone}


class TimeTable(db.Model):
    __tablename__ = 'timetable'

    id = db.Column(db.Integer(), primary_key=True)
    classroom = db.Column(db.Integer(), db.ForeignKey('classroom.id'))
    dayofweek = db.Column(db.String())
    starttime = db.Column(db.Time())
    endtime = db.Column(db.Time())
    lecture = db.Column(db.Integer(), db.ForeignKey('lecture.id'))

    def to_json(self):
        cur_room = Classroom.query.filter_by(id=self.classroom).first()
        cur_lecture = Lecture.query.filter_by(id=self.lecture).first()
        cur_course = Course.query.filter_by(id=cur_lecture.course).first()
        cur_lecturer= Lecturer.query.filter_by(id=cur_lecture.lecturer).first().to_json()
        return {'id': self.id, 'classroom': cur_room.building, 'dayofweek': self.dayofweek, 'starttime': self.starttime, 'endtime': self.endtime, 'lecture': f"{cur_course.name}by{cur_lecturer['fullname']}"}


class Lecture(db.Model):

    __tablename__ = 'lecture'

    id = db.Column(db.Integer(), primary_key=True)
    course = db.Column(db.Integer(), db.ForeignKey('course.id'))
    lecturer = db.Column(db.Integer(), db.ForeignKey('lecturer.id'))


class Lecturer(db.Model):

    __tablename__ = 'lecturer'

    id = db.Column(db.Integer(), primary_key=True)
    usertype = db.Column(db.String(1), db.ForeignKey('user.usertype'), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    office = db.Column(db.String(200))
    __table_args__ = (db.CheckConstraint("usertype='L'", name="Lecturer User"),)

    def to_json(self):
        cur_user = User.query.filter_by(id=self.user).first()
        return {'id': self.id, 'fullname': cur_user.fullname(), "phone": cur_user.phone, "email": cur_user.email, 'office': self.office, "admin": cur_user.isAdmin }


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.String())
    name = db.Column(db.String())
    description = db.Column(db.Text())
    level = db.Column(db.Integer())
    credit = db.Column(db.Integer())

    def to_json(self):
        return {'id': self.id, 'number': self.number, 'name': self.name, 'description': self.description, 'level': self.level, 'credit': self.credit}


class student_course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student = db.Column(db.Integer(), db.ForeignKey('student.id'))
    course = db.Column(db.Integer(), db.ForeignKey('course.id'))


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer(), primary_key=True)
    usertype = db.Column(db.String(1), db.ForeignKey('user.usertype'), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    department = db.Column(db.String(16))
    year = db.Column(db.Integer())
    __table_args__ = (db.CheckConstraint("usertype='S'", name='Student User'),)

    def to_json(self):
        cur_user = User.query.filter_by(id=self.user).first()
        return {'id': self.id, 'fullname': cur_user.fullname(), "phone": cur_user.phone, "email": cur_user.email, "year": self.year, 'department': self.department }


class Classroom(db.Model):
    __tablename__ = 'classroom'

    id = db.Column(db.Integer(), primary_key=True)
    building = db.Column(db.String(), unique=True)
    size = db.Column(db.Integer())
    type = db.Column(db.String())

    def to_json(self):
        return {'id': self.id, 'building': self.building, 'size': self.size, 'type': self.type}


class Sessions(db.Model):
    
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)