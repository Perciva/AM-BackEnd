from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database import db, sess
from sqlalchemy.orm import relationship
from datetime import datetime


class Period(db.Model):
    __tablename__ = 'periods'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column('description', db.String(255))
    start = db.Column('start', db.Date)
    end = db.Column('end', db.Date)
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)

    special_shift_relationship = db.relationship("SpecialShift", back_populates="period", cascade="all, delete, merge, "
                                                                                                  "save-update")
    assistant = db.relationship("Assistant", back_populates="period", cascade="all, delete, merge, save-update")
    leader = db.relationship("Leader", back_populates="period", cascade="all, delete, merge, save-update")
    holiday = db.relationship("Holiday", back_populates="period", cascade="all, delete, merge, save-update")

    def __init__(self, description, start, end, created_at, updated_at):
        self.description = description
        self.end = end
        self.start = start
        self.created_at = created_at
        self.updated_at = updated_at

    # def __str__(self):
    #     output = "id:{},description:{}, start:{}, end:{}, created_at:{}, updated_at:{}"
    #     formated = output.format(self.id, self.description, self.start, self.end, self.created_at, self.updated_at)
    #     return formated


def insert(description, start, end):
    per = Period(description, start, end, datetime.now(), datetime.now())
    sess.add(per)
    # sess.flush()
    # print(per.id)
    sess.commit()


def getAllPeriod():
    users = sess.query(Period).all()
    res = list()
    for user in users:
        res.append(user)
    # print(res)
    return res

def getPeriodById(period_id):
    period = sess.query(Period).filter_by(id=period_id).one_or_none()

    if period is None:
        return "Period with id " + str(period_id) + " Not Found!"
    else:
        return period


def delete(id):
    sess.query(Period).filter_by(id=id).delete()
    sess.commit()
    return True


def update(id, description, start, end):
    user = sess.query(Period).filter_by(id=id).one()
    if user != []:
        user.description = description
        user.start = start
        user.end = end
        user.updated_at = datetime.now()

        sess.add(user)
        sess.commit()

        return True
    else:
        return False

    pass
