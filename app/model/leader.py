from sqlalchemy import and_
from app.database import db, sess
from datetime import datetime
from app.model.period import Period


class Leader(db.Model):
    __tablename__ = 'leaders'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey('periods.id', ondelete="CASCADE"))
    initial = db.Column('initial', db.String(7))
    name = db.Column('name', db.String(255))
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    period = db.relationship("Period", back_populates="leader")
    assistant = db.relationship("Assistant", back_populates="leader", cascade="all, delete, merge, save-update")

    def __init__(self, period_id, initial, name, created_at, updated_at):
        self.period_id = period_id
        self.initial = initial
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at


def insert(period_id, initial, name):
    leader = sess.query(Leader).filter_by(initial=initial).filter_by(period_id=period_id).one_or_none()
    if leader is None:
        l = Leader(period_id, initial, name, datetime.now(), datetime.now())
        sess.add(l)
        sess.commit()
        return "Success"''
    else:
        return "Leader With Initial " + initial + " Already Exists In The Selected Period!"


def delete(id):
    l = sess.query(Leader).filter_by(id=id).one_or_none()
    sess.delete(l)
    sess.commit()
    return True


def update(id,period_id, initial, name):
    l = sess.query(Leader).filter_by(id=id).one_or_none()

    if l is None:
        return "Leader with ID "+id+" Not Found!"
    else:

        checkleader = sess.query(Leader).filter_by(period_id=period_id).filter_by(initial = initial).one_or_none()
        if checkleader is None or l.initial == initial:
            l.initial = initial
            l.name = name
            l.updated_at = datetime.now()

            sess.add(l)
            sess.commit()

            return "Success"
        else:
            return "Leader With Initial " + initial + " Already Exists In The Selected Period!"



def getLeaderByID(id):
    l = sess.query(Leader).filter_by(id=id).one_or_none()
    return l


def getLeaderByPeriodID(period_id):
    ls = sess.query(Leader).filter(Leader.period_id == period_id).all()
    return ls


def getLeaderByInitialAndPeriod(initial, period_id):
    ls = sess.query(Leader).filter(and_(Leader.initial.like(initial), Leader.period_id.like(period_id))).one_or_none()
    return ls
