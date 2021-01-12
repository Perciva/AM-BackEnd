from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database  import Base, sess
from datetime import datetime

class Holiday(Base):
    __tablename__ = 'holidays'
    id = Column(Integer, primary_key = True)
    period_id = Column('period_id', Integer)
    description = Column('description', String(255))
    date = Column('date', Date)
    created_at = Column('created_at', TIMESTAMP)
    updated_at = Column('updated_at', TIMESTAMP)


    def __init__(self, period_id, description, date, created_at, updated_at):
        self.period_id = period_id
        self.description = description
        self.date = date
        self.created_at = created_at
        self.updated_at = updated_at

def insert(period_id, description, date):
    holiday = Holiday(period_id, description,date,datetime.now(),datetime.now())
    sess.add(holiday)
    sess.commit()
    return True

def delete(id):
    Holiday.query.filter_by(id=id).delete()
    sess.commit()
    return True

def update(id, description, date):
    holiday = sess.query(Holiday).filter_by(id=id).one()

    if holiday != []:
        holiday.date = date
        holiday.description = description
        holiday.updated_at = datetime.now()

        sess.add(holiday)
        sess.commit()

        return True
    else:
        return False

def getAllHolidayByPeriodID(period_id):
    holiday = sess.query(Holiday).filter_by(period_id = period_id).all()
    return holiday




