from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database import db, sess
from sqlalchemy.orm import relationship
from datetime import datetime


class SpecialShift(db.Model):
    __tablename__ = 'special_shifts'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column('period_id', db.Integer, db.ForeignKey("periods.id"))
    description = db.Column('description', db.String(255))
    assistant_ids = db.Column('assistant_ids', db.TEXT)
    date = db.Column('date', db.Date)
    _in = db.Column('in', db.Time)
    _out = db.Column('out', db.Time)
    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)
    # period = db.relationship("Period", back_populates='special_shift_relationship')

    def __init__(self, period_id, description, assistant_ids, date, _in, _out):
        self.period_id = period_id
        self.description = description
        self.assistant_ids = assistant_ids
        self._in = _in
        self._out = _out
        self.date = date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def insert(period_id, description, assistant_ids, date, _in, _out):
    ss = SpecialShift(period_id, description, assistant_ids, date, _in, _out)
    sess.add(ss)
    sess.commit()
    return True
