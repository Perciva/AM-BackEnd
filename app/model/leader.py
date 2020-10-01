from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database  import Base

class Leader(Base):
    __tablename__ = 'leaders'
    id = Column(Integer, primary_key = True)
    period_id = Column('period_id', Integer)
    initial = Column('initial', String(6), unique=True )
    name = Column('name', String(255))
    created_at = Column('created_at', TIMESTAMP)
    updated_at = Column('updated_at', TIMESTAMP)


    def __init__(self, id, period_id, initial, name, created_at, updated_at):
        self.id=id
        self.period_id = period_id
        self.initial = initial
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

