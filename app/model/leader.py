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
    ls = sess.query(Leader).filter_by(period_id=period_id).all() 
    return ls


