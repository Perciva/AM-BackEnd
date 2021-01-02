from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('mysql+pymysql://root:@localhost/testing', echo=True)
sess = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = sess.query_property()

def init_db():
    import app.model.leader
    from app.model import leader, assistant,period

    # i= leader.Leader(1,123,'LI','Alicia',datetime.now(),datetime.now())
    # l= assistant.Assistant(1,123,1,'AB','Alberic',datetime.now(),datetime.now())
    # p = period.Period("odd semester 19/20","2019-01-01","2019-07-01",datetime.now(),datetime.now())
    # sess.add(l)
    # sess.add(i)
    # print("THIS")
    # sess.add(p)
    sess.commit()

    Base.metadata.create_all(bind=engine)


