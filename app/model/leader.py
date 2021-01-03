from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database  import Base, sess
from datetime import datetime

class Leader(Base):
    __tablename__ = 'leaders'
    id = Column(Integer, primary_key = True)
    period_id = Column('period_id', Integer)
    initial = Column('initial', String(6), unique=True)
    name = Column('name', String(255))
    created_at = Column('created_at', TIMESTAMP)
    updated_at = Column('updated_at', TIMESTAMP)


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
    Leader.query.filter_by(id=id).delete()
    sess.commit()
    
def update(id, period_id, initial, name):
    l = sess.query(Leader).filter_by(id=id).one()

    if l != []:
        l.period_id = period_id
        l.initial = initial
        l.name = name
        l.updated_at = datetime.now()

        sess.add(l)
        sess.commit()

        return True
    else:
        return False

def getAllLeader():
    ls = sess.query(Leader).all() 
    return ls

def getLeaderByID(id):
    l = sess.query(Leader).filter_by(id=id).one()
    # print(l.name)
    return l


