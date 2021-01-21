from sqlalchemy import Column, Integer, String, TIMESTAMP, tuple_
from app.database import db, sess
from datetime import datetime
from sqlalchemy import func


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


def insert(assistant_initial, period_id, date, _in, _out):
    from app.model.assistant import Assistant

    ast = sess.query(Assistant).filter_by(initial=assistant_initial).filter_by(period_id=period_id).one_or_none()

    if ast is None:
        return "Assistant with initial " + assistant_initial + " Not Found In The Selected Period!"
    else:
        att = sess.query(Attendance).filter_by(date=date).filter_by(assistant_id=ast.id).one_or_none()
        if att is not None:
            att._in = _in
            att._out = _out
            att.updated_at = datetime.now()
            sess.add(att)
            sess.commit()

        else:
            attendance = Attendance(ast.id, date, _in, _out, "", "", "", "", "", "")
            sess.add(attendance)
            sess.commit()

        return "Success"


def update(id, in_permission, out_permission, special_permission,
           in_permission_description,
           out_permission_description, special_permission_description):
    attendance = sess.query(Attendance).filter_by(id=id).one_or_none()
    if attendance is None:
        return "Attendance with id " + str(id) + " Not Found!"
    else:
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


def getAttendanceSummary(assistant_id, period_id, leader_id, start_date, end_date):
    inpermission = sess.query(Attendance.in_permission, func.count(Attendance.in_permission)).group_by(
        Attendance.in_permission).filter(Attendance.assistant_id == assistant_id).all()

    for i in inpermission:
        print(i.in_permission)



def getAllAttendanceByDate(start_date, end_date, assistant_id):
    attendance = sess.query(Attendance).filter_by(assistant_id=assistant_id).order_by(Attendance.date.asc()).all()

    result = list()
    if attendance == []:
        return None
    else:
        for att in attendance:
            res = dict()

            startdate = datetime.date(datetime.strptime(start_date, "%Y-%m-%d"))
            enddate = datetime.date(datetime.strptime(end_date, "%Y-%m-%d"))

            if (att.date >= startdate and att.date <= enddate):
                res["attendance"] = att
                res["special_shift"] = None

                from app.model.special_shift import SpecialShift
                # print(att.assistant.initial)
                ss = sess.query(SpecialShift).filter(
                    SpecialShift.assistant_ids.contains(att.assistant.initial)).order_by(SpecialShift.date.asc()).all()

                ssresult = list()
                for s in ss:
                    if (s.date >= startdate and s.date <= enddate):
                        print(s.date)
                        ssresult.append(s)

                if ssresult != []:
                    res["special_shift"] = ssresult
                result.append(res)

        return result
