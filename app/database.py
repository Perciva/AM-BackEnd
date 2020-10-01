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
    from app.model import leader

    # l= leader.Leader(1,123,'LI','Alicia',datetime.now(),datetime.now())

    sess.add(l)
    sess.commit()

    Base.metadata.create_all(bind=engine)


