from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database  import Base, sess
from datetime import datetime

class Assistant(Base):
    __tablename__ = 'assistants'
    id = Column(Integer, primary_key = True)
    period_id = Column('period_id', Integer)
    leader_id = Column('leader_id', Integer)
    initial = Column('initial', String(6), unique=True )
    name = Column('name', String(255))
    created_at = Column('created_at', TIMESTAMP)
    updated_at = Column('updated_at', TIMESTAMP)

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

def update(id, period_id, leader_id, initial, name):
    ast = sess.query(Assistant).filter_by(id=id).one()

    if ast != []:
        ast.period_id = period_id
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
    





