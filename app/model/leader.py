from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import db, sess
from datetime import datetime
from app.model.period import Period


class Leader(db.Model):
    __tablename__ = 'leaders'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey('periods.id'))
    initial = db.Column('initial', db.String(6), unique=True)
    name = db.Column('name', db.String(255))
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    period = db.relationship("Period", back_populates="leader")
    assistant = db.relationship("Assistant", back_populates="leader")

    def __init__(self, period_id, initial, name, created_at, updated_at):
        self.period_id = period_id
        self.initial = initial
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at


def insert(period_id, initial, name):
    l = Leader(period_id, initial, name, datetime.now(), datetime.now())
    sess.add(l)
    sess.commit()
    return True


def delete(id):
    sess.query.filter_by(id=id).delete()
    sess.commit()
    return True


def update(id, initial, name):
    l = sess.query(Leader).filter_by(id=id).one()

    if l != []:
        l.initial = initial
        l.name = name
        l.updated_at = datetime.now()

        sess.add(l)
        sess.commit()

        return True
    else:
        return False


def getLeaderByID(id):
    l = sess.query(Leader).filter_by(id=id).one()
    return l


def getLeaderByPeriodID(period_id):
    from pprint import pprint
    ls = sess.query(Leader).filter(Leader.period_id == Period.id).all()

    for a in ls:
        print(a.period.description)

    return ls


def getLeaderByInitial(initial):
    ls = sess.query(Leader).filter_by(initial=initial).one_or_none()
    return ls
