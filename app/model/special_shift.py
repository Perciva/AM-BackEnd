from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database import db, sess
from sqlalchemy.orm import relationship
from datetime import datetime


class SpecialShift(db.Model):
    __tablename__ = 'special_shifts'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey("periods.id", ondelete="CASCADE"))
    description = db.Column('description', db.String(255))
    assistant_ids = db.Column('assistant_ids', db.TEXT)
    date = db.Column('date', db.Date)
    _in = db.Column('in', db.Time)
    _out = db.Column('out', db.Time)
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)
    period = db.relationship("Period", back_populates='special_shift_relationship')

    def __init__(self, period_id, description, assistant_ids, date, _in, _out):
        self.period_id = period_id
        self.description = description
        self.assistant_ids = assistant_ids
        self._in = _in
        self._out = _out
        self.date = date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def insert(period_id, description, assistant_ids, date, _in, _out):
    from app.model.assistant import Assistant

    error = ""
    if assistant_ids != "ALL":
        ast = assistant_ids.split(',')
        ast = map(trim, ast)

        for a in ast:
            res = sess.query(Assistant).filter_by(initial=a).filter_by(period_id=period_id).one_or_none()
            if res is None:
                error = error + "Assistant With Initial " + str(a) + " Not Found In The Selected Period!"

    if error == "":
        ss = SpecialShift(period_id, description, assistant_ids, date, _in, _out)
        sess.add(ss)
        sess.commit()
        return "Success"
    else:
        return error


def delete(id):
    ss = sess.query(SpecialShift).filter_by(id=id).one_or_none()

    if ss is None:
        return "Special Shift with id "+ str(id) + " Not Found!"
    else:
        sess.delete(ss)
        sess.commit()
        return "Success"


def update(id, period_id, description, assistant_ids, date, _in, _out):
    ss = sess.query(SpecialShift).filter_by(id=id).one()

    if ss:
        from app.model.assistant import Assistant
        error = ""
        if assistant_ids != "ALL":
            ast = assistant_ids.split(',')
            ast = map(trim, ast)

            error = ""
            for a in ast:
                res = sess.query(Assistant).filter_by(initial=a).filter_by(period_id=period_id).one_or_none()
                if res is None:
                    error = error + "Assistant With Initial " + str(a)+ " Not Found In The Selected Period!"

        if error == "":
            ss.period_id = period_id
            ss.description = description
            ss.assistant_ids = assistant_ids
            ss._in = _in
            ss._out = _out
            ss.date = date
            ss.updated_at = datetime.now()

            sess.add(ss)
            sess.commit()
            return "Success"
        else:
            return error
    else:
        return "Special Shift with Id " + str(id) + " Not Found!"


def getAllSpecialShiftByPeriodId(period_id):
    ss = sess.query(SpecialShift).filter_by(period_id=period_id).all()

    return ss


def trim(s):
    return s.strip()
