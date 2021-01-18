from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import db, sess
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    assistant_id = db.Column('assistant_id', db.Integer, db.ForeignKey('assistants.id', ondelete="CASCADE"))
    # assistant = db.relationship("Assistant", back_populates="attendance")
    date = db.Column('date', db.Date)
    _in = db.Column('in', db.Time)
    _out = db.Column('out', db.Time)

    in_permission = db.Column('in_permission', db.Enum('', 'IT', 'LM', 'TM', 'TL'))
    out_permission = db.Column('out_permission', db.Enum('', 'IP', 'LP', 'TL'))
    special_permission = db.Column('special_permission', db.Enum('', 'CT', 'SK', 'AP', 'TL'))

    in_permission_description = db.Column('in_permission_description', db.String(255))
    out_permission_description = db.Column('out_permission_description', db.String(255))
    special_permission_description = db.Column('special_permission_description', db.String(255))

    created_at = db.Column('created_at', db.TIMESTAMP)
    updated_at = db.Column('updated_at', db.TIMESTAMP)


    def __init__(self, assistant_id, date, _in, _out, in_permission, out_permission, special_permission,
                 in_permission_description, out_permission_description, special_permission_description):
        self.assistant_id = assistant_id
        self.date = date
        self._in = _in
        self._out = _out
        self.in_permission = in_permission
        self.in_permission_description = in_permission_description
        self.out_permission = out_permission
        self.out_permission_description = out_permission_description
        self.special_permission = special_permission
        self.special_permission_description = special_permission_description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def insert(assistant_id, date, _in, _out, in_permission, out_permission, special_permission, in_permission_description,
           out_permission_description, special_permission_description):
    pass
