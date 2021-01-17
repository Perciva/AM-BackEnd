from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from app.database  import db, sess
from sqlalchemy.orm import relationship
from datetime import datetime
import app.model.leader

class Assistant(db.Model):
    
    __tablename__ = 'assistants'
    id = db.Column(db.Integer, primary_key = True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey('periods.id'))
    leader_id = db.Column('leader_id', db.Integer, db.ForeignKey('leaders.id'))
    initial = db.Column('initial', db.String(6), unique=True)
    name = db.Column('name', db.String(255))
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    period = db.relationship("Period", back_populates="assistant")
    leader = db.relationship("Leader", back_populates="assistant")
    # shift = db.relationship("Shift", back_populates="assistant")
    # attendance = db.relationship("Attendance", back_populates="assistant")

    def __init__(self, period_id, leader_id, initial, name, created_at, updated_at):
        self.period_id = period_id
        self.leader_id = leader_id
        self.initial = initial
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at


def insert(period_id, leader_id, initial, name):
    ast = Assistant(period_id, leader_id, initial, name,datetime.now(),datetime.now())
    sess.add(ast)
    sess.commit()
    return True


def delete(id):
    Assistant.query.filter_by(id=id).delete()
    sess.commit()
    return True

def update(id, leader_id, initial, name):
    ast = sess.query(Assistant).filter_by(id=id).one()

    if ast != []:
        ast.leader_id = leader_id
        ast.initial = initial
        ast.name = name
        ast.updated_at = datetime.now()

        sess.add(ast)
        sess.commit()

        return True
    else:
        return False

def getAssistantByID(id):
    ast = sess.query(Assistant).filter_by(id=id).one()
    return ast

def getAllAssistant():
    ast = sess.query(Assistant).all()
    
    return ast

def getAssistantByPeriodID(period_id):
    ast = sess.query(Assistant).filter_by(period_id = period_id).all()
    return ast

# def getAssistantWithLeaderByPeriod():
#     ast = sess.query(Assistant).join(Leader)


    





