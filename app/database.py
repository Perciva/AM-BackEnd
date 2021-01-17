from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.app import app
from ariadne import QueryType, MutationType

# from flask_migrate import Migrate
engine = create_engine('mysql+pymysql://root:@localhost/testing', 
                        echo=True, pool_size=1000, max_overflow=0)
sess = scoped_session(sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine))

db = SQLAlchemy(app)
Base = declarative_base(bind=engine)
Base.query = sess.query_property()
# def init_sql(engine):
#     pass
query = QueryType()
mutation = MutationType()

# migrate = Migrate(app,db)
def init_db():
    from app.model.leader import Leader
    from app.model.attendance import Attendance
    from app.model.shift import Shift
    from app.model.leader import Leader
    from app.model.assistant import Assistant
    from app.model.special_shift import SpecialShift
    from app.model.period import Period
    #
    # p = Period("odd semester 19/20","2019-01-01","2019-07-01",datetime.now(),datetime.now())
    # i= Leader(4,'LI','Alicia',datetime.now(),datetime.now())
    # l= Assistant(4,1,'AB','Alberic',datetime.now(),datetime.now())
    # sess.add(p)
    # sess.add(l)
    # sess.add(i)
    # print("THIS")
    # sess.commit()
    #
    db.create_all()
