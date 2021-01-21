from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from app.database import db, sess
from sqlalchemy.orm import relationship
from datetime import datetime


class Assistant(db.Model):
    __tablename__ = 'assistants'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey('periods.id', ondelete="CASCADE"))
    leader_id = db.Column('leader_id', db.Integer, db.ForeignKey('leaders.id', ondelete="CASCADE"))
    initial = db.Column('initial', db.String(7))
    name = db.Column('name', db.String(255))
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    period = db.relationship("Period", back_populates="assistant")
    leader = db.relationship("Leader", back_populates="assistant")
    shift = db.relationship("Shift", back_populates="assistant", cascade="all, delete, merge, save-update")
    attendance = db.relationship("Attendance", back_populates="assistant", cascade="all, delete, merge, save-update")

    def __init__(self, period_id, leader_id, initial, name):
        self.period_id = period_id
        self.leader_id = leader_id
        self.initial = initial
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def insert(period_id, leader_id, initial, name):
    ast = sess.query(Assistant).filter_by(period_id=period_id).filter_by(initial=initial).one_or_none()

    if ast is None:
        ast = Assistant(period_id, leader_id, initial, name)
        sess.add(ast)
        sess.commit()
        return "Success"
    else:
        # from app.tools import color
        # color.pred("Assistant With Initial " + initial + " Already Exists In The Selected Period!")
        return "Assistant With Initial " + initial + " Already Exists In The Selected Period!"


def insertByLeaderInitial(period_id, leader_initial, initial, name):
    from app.model.leader import Leader
    leader = sess.query(Leader).filter_by(initial=leader_initial).filter_by(period_id=period_id).one_or_none()
    if leader is None:
        return "There Is No Leader " + leader_initial + "In The Selected Period!"
    else:
        return insert(period_id, leader.id, initial, name)


def delete(id):
    ast = sess.query(Assistant).filter_by(id=id).one()
    sess.delete(ast)
    sess.commit()
    return True


def update(id, period_id, leader_id, initial, name):
    ast = sess.query(Assistant).filter_by(id=id).one_or_none()

    if ast is None:
        return "Assistant with ID "+id+" Not Found!"
    else:
        checkast = sess.query(Assistant).filter_by(period_id=period_id).filter_by(initial=initial).one_or_none()
        if checkast is None or ast.initial == initial:
            ast.leader_id = leader_id
            ast.initial = initial
            ast.name = name
            ast.updated_at = datetime.now()

            sess.add(ast)
            sess.commit()

            return "Success"
        else:
            return "Assistant With Initial " + initial + " Already Exists In The Selected Period!"



def getAssistantByID(id):
    ast = sess.query(Assistant).filter_by(id=id).one()
    return ast


def getAllAssistant():
    ast = sess.query(Assistant).all()

    return ast


def getAssistantByPeriodID(period_id):
    ast = sess.query(Assistant).filter_by(period_id=period_id).all()
    return ast

# def getAssistantWithLeaderByPeriod():
#     ast = sess.query(Assistant).join(Leader)
