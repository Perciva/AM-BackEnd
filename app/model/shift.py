from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import db, sess
from datetime import datetime


class Shift(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True)
    assistant_id = db.Column('assistant_id', db.Integer, db.ForeignKey('assistants.id', ondelete="CASCADE"))
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
    ss = sess.query(Shift).filter_by(assistant_id=assistant_id).filter_by(day=day).one_or_none()

    if ss is None:
        shift = Shift(assistant_id, day, _in, _out)
        sess.add(shift)
        sess.commit()
    else:
        ss._in = _in
        ss._out = _out
        ss.updated_at = datetime.now()
        sess.add(ss)
        sess.commit()
    return True


def delete(id):
    sh = sess.query(Shift).filter_by(id=id).one()
    sess.delete(sh)

    sess.commit()
    return True


def deleteAllAssistantShift(assistant_id):
    sess.query(Shift).filter(Shift.assistant_id==assistant_id).delete(synchronize_session=False)
    sess.commit()

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


def insertByAssistatInitial(assistant_initial, day, _in, _out):
    from app.model.assistant import Assistant

    ast = sess.query(Assistant).filter_by(initial=assistant_initial).one_or_none()
    if ast:
        shift = Shift(ast.id, day, _in, _out)
        sess.add(shift)
        sess.commit()

        return "Success"
    else:
        return "Assistant "+ assistant_initial+" Not Found!"
