from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import db, sess
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    assistant_id = db.Column('assistant_id', db.Integer, db.ForeignKey('assistants.id', ondelete="CASCADE"))

    date = db.Column('date', db.Date)
    _in = db.Column('in', db.Time)
    _out = db.Column('out', db.Time)

    in_permission = db.Column('in_permission', db.Enum('', 'IT', 'LM', 'TM', 'TL'))
    out_permission = db.Column('out_permission', db.Enum('', 'IP', 'LP', 'TL'))
    special_permission = db.Column('special_permission', db.Enum('', 'CT', 'SK', 'AP', 'TL'))

    in_permission_description = db.Column('in_permission_description', db.String(255))
    out_permission_description = db.Column('out_permission_description', db.String(255))
    special_permission_description = db.Column('special_permission_description', db.String(255))

    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    assistant = db.relationship("Assistant", back_populates="attendance")

    def __init__(self, assistant_id, date, _in, _out, in_permission, out_permission, special_permission,
                 in_permission_description, out_permission_description, special_permission_description):
        self.assistant_id = assistant_id
        self.date = date
        self._in = _in
        self._out = _out
        self.in_permission = in_permission
        self.in_permission_description = in_permission_description
        self.out_permission = out_permission
        self.out_permission_description = out_permission_description
        self.special_permission = special_permission
        self.special_permission_description = special_permission_description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def insert(assistant_id, date, _in, _out, in_permission, out_permission, special_permission, in_permission_description,
           out_permission_description, special_permission_description):
    attendance = Attendance(assistant_id, date, _in, _out, in_permission, out_permission, special_permission,
                            in_permission_description, out_permission_description, special_permission_description)
    sess.add(attendance)
    sess.commit()

    return "Success"

def update(id, assistant_id, date, _in, _out, in_permission, out_permission, special_permission, in_permission_description,
           out_permission_description, special_permission_description):
    attendance = sess.query(Attendance).filter_by(id=id).one_or_none()
    if attendance is None:
        return "Attendance with id "+ str(id) + " Not Found!"
    else:
        attendance.assistant_id = assistant_id
        attendance.date = date
        attendance._in = _in
        attendance._out = _out
        attendance.in_permission = in_permission
        attendance.in_permission_description = in_permission_description
        attendance.out_permission = out_permission
        attendance.out_permission_description = out_permission_description
        attendance.special_permission = special_permission
        attendance.special_permission_description = special_permission_description
        attendance.updated_at = datetime.now()

        sess.add(attendance)
        sess.commit()

        return "Success"

def delete(id):
    attendance = sess.query(Attendance).filter_by(id=id).one_or_none()
    if attendance is None:
        return "Attendance with id " + str(id) + " Not Found!"
    else:
        sess.delete(attendance)
        sess.commit()
        return "Success"

def getAttendanceByPeriodId(period_id):
    attendance = sess.query(Attendance).filter_by(period_id=period_id).all()
    if attendance == []:
        return "Attendance with Period ID " + str(period_id) + " Not Found!"
    else:
        return attendance
