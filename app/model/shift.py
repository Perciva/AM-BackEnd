from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import db, sess
from datetime import datetime


class Shift(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True)
    assistant_id = db.Column('assistant_id', db.Integer, db.ForeignKey('assistants.id'))
    day = db.Column('day', db.Integer)
    _in = db.Column('in', db.Time)
    _out = db.Column('out', db.Time)
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    assistant = db.relationship("Assistant", back_populates="shift")

    def __init__(self, assistant_id, day, _in, _out):
        self.assistant_id = assistant_id
        self.day = day
        self._in = _in
        self._out = _out
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def insert(assistant_id, day, _in, _out):
    shift = Shift(assistant_id, day, _in, _out)
    sess.add(shift)
    sess.commit()
    return True


def delete(id):
    print(id)
    shift = sess.query(Shift).filter_by(id=id).delete()
    sess.delete(shift)

    sess.commit()
    return True


def deleteAllAssistantShift(assistant_id):
    Shift.query.filter_by(assistant_id=assistant_id).all().delete()
    sess.commmit()
    return True


def update(id, assistant_id, day, _in, _out):
    shift = sess.query(Shift).filter_by(id=id).one()

    if shift:
        shift.assistant_id = assistant_id
        shift.day = day
        shift._in = _in
        shift._out = _out
        shift.updated_at = datetime.now()

        sess.add(shift)
        sess.commit()

        return True
    else:
        return False


def getAssistantShifts(assistant_id):
    shift = sess.query(Shift).filter_by(assistant_id=assistant_id).all()
    return shift
