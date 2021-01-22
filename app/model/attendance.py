from sqlalchemy import Column, Integer, String, TIMESTAMP, and_, or_
from app.database import db, sess
from datetime import datetime
from sqlalchemy import func
from app.tools import color


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


def getAttendanceSummary(assistant_id, period_id, start_date, end_date):
    from app.model.shift import Shift
    from app.model.special_shift import SpecialShift
    from app.model.holiday import Holiday
    from app.model.assistant import Assistant

    ast = sess.query(Assistant).filter(Assistant.id == assistant_id).one_or_none()

    if ast is None:
        return None

    initial = ast.initial
    # color.pred(initial)
    inpermission = sess.query(Attendance.in_permission, func.count(Attendance.in_permission).label('count')).group_by(
        Attendance.in_permission).filter(Attendance.assistant_id == assistant_id).filter(
        and_(Attendance.date >= start_date, Attendance.date <= end_date)).all()

    outpermission = sess.query(Attendance.out_permission,
                               func.count(Attendance.out_permission).label('count')).group_by(
        Attendance.out_permission).filter(Attendance.assistant_id == assistant_id).filter(
        and_(Attendance.date >= start_date, Attendance.date <= end_date)).all()

    specialpermission = sess.query(Attendance.special_permission,
                                   func.count(Attendance.special_permission).label('count')).group_by(
        Attendance.special_permission).filter(Attendance.assistant_id == assistant_id).filter(
        and_(Attendance.date >= start_date, Attendance.date <= end_date)).all()

    unverifiedcount = sess.query(Attendance).filter(
        Attendance.in_permission == "").filter(Attendance.out_permission == "").filter(
        Attendance.special_permission == "").filter(
        and_(Attendance.date >= start_date, Attendance.date <= end_date)).group_by(Attendance.date).all()

    result = dict()

    inPermissionResult = dict()
    outPermissionResult = dict()
    specialPermissionResult = dict()
    unverifiedresult = 0;

    for u in unverifiedcount:
        # color.pgreen(str(u.date))
        checkholiday = sess.query(Holiday).filter(Holiday.date == u.date).filter(
            Holiday.period_id == period_id).one_or_none()

        if checkholiday is not None:  # kalau hari itu holiday
            continue
        else:
            specialshift = sess.query(SpecialShift).filter(SpecialShift.period_id == period_id).filter(or_(
                SpecialShift.assistant_ids.contains(initial), SpecialShift.assistant_ids == "ALL")).filter(
                SpecialShift.date == u.date).order_by(SpecialShift.updated_at.desc()).first()

            if specialshift is not None:  # kalau hari itu ada special shift
                shift_in = specialshift._in
                shift_out = specialshift._out

                if (u._in > shift_in) or (u._out < shift_out):
                    unverifiedresult += 1
                    continue
                # color.pred(str(u._in))
                # color.pred(str(shift_in))
                # color.pred(str(u._in > shift_in))
            else:  # kalau tak ada special shift, check shift biasa
                weekday = u.date.weekday()
                # color.pmagenta(str(weekday))
                weekday += 1
                checkshift = sess.query(Shift).filter(Shift.assistant_id == assistant_id).filter(
                    Shift.day == weekday).one_or_none()

                if checkshift is not None:
                    shift_in = checkshift._in
                    shift_out = checkshift._out

                    if (u._in > shift_in) or (u._out < shift_out):
                        unverifiedresult += 1
                        continue

    for i in inpermission:
        if i.in_permission == "":
            pass
        else:
            inPermissionResult[i.in_permission] = i.count

    for i in outpermission:
        if i.out_permission == "":
            pass
        else:
            outPermissionResult[i.out_permission] = i.count

    for i in specialpermission:
        if i.special_permission == "":
            pass
        else:
            specialPermissionResult[i.special_permission] = i.count
        # print(dir(i))
    # color.pred(str(inPermissionResult))
    result["assistant"] = initial
    result["in"] = inPermissionResult
    result["out"] = outPermissionResult
    result["special"] = specialPermissionResult
    result["unverified"] = unverifiedresult
    result["leader"] = ast.leader.initial

    return result


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

                ss = sess.query(SpecialShift).filter(or_(
                    SpecialShift.assistant_ids.contains(att.assistant.initial),
                    SpecialShift.assistant_ids == "ALL")).order_by(SpecialShift.date.asc()).all()

                ssresult = list()
                for s in ss:
                    if (s.date >= startdate and s.date <= enddate):
                        print(s.date)
                        ssresult.append(s)

                if ssresult != []:
                    res["special_shift"] = ssresult
                result.append(res)

        return result
