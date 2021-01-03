from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database  import Base, sess
from datetime import datetime

class Period(Base):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key = True)
    description = Column('description', String(255))
    start = Column('start', Date)
    end = Column('end', Date)
    created_at = Column('created_at', TIMESTAMP)
    updated_at = Column('updated_at', TIMESTAMP)


    def __init__(self,description, start, end, created_at, updated_at):
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
    per = Period(description,start,end, datetime.now(), datetime.now())
    sess.add(per)
    # sess.flush()
    # print(per.id)
    sess.commit()

def getAllPeriod():
    users = sess.query(Period).all()
    res = list()
    for user in users:
        # print(user)
        res.append(user)

    # print(res)
    return res

def delete(id):
    Period.query.filter_by(id=id).delete()
    sess.commit()
    pass

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






