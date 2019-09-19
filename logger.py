import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
# Create db in memory
engine = sql.create_engine('sqlite:///:memory:', echo=True)

class Log(Base):
    __tablename__ = "transaction_log"

    id = sql.Column('ID', sql.Integer, primary_key=True)
    dateTime = sql.Column('DATETIME', sql.DateTime)
    endPoint = sql.Column('ENDPOINT', sql.String)
    message = sql.Column('MESSAGE', sql.String)

# Class used to log data to DB
class Logger():
    autoID = 1
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def write(self, message, endpoint):
        Session = sessionmaker(bind=engine)
        session = Session()
        log = Log()
        log.id = self.autoID
        log.datetime = datetime.datetime.now()
        log.endpoint = endpoint
        log.message = str(message)
        session.add(log)
        session.commit()
        session.close()
        self.autoID += 1

    def read_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        logs = session.query(Log).all()
        # TODO: return the logs
        # for l in logs:
        # print(str(l))
        session.close()
