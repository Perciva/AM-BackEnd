from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database import db, sess
from datetime import datetime


class Holiday(db.Model):
    __tablename__ = 'holidays'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey('periods.id'))
    description = db.Column('description', db.String(255))
    date = db.Column('date', db.Date)
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    period = db.relationship("Period", back_populates="holiday")

    def __init__(self, period_id, description, date, created_at, updated_at):
        self.period_id = period_id
        self.description = description
        self.date = date
        self.created_at = created_at
        self.updated_at = updated_at


def insert(period_id, description, date):
    holiday = Holiday(period_id, description, date, datetime.now(), datetime.now())
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
    holiday = sess.query(Holiday).filter_by(period_id=period_id).all()
    return holiday
