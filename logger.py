import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
# Create db in memory
engine = sql.create_engine('sqlite:///pythonsqlite.db', echo=True)

class Log(Base):
    __tablename__ = "transaction_log"

    id = sql.Column('ID', sql.Integer, primary_key=True)
    dateTime = sql.Column('DATETIME', sql.DateTime)
    endPoint = sql.Column('ENDPOINT', sql.String)
    message = sql.Column('MESSAGE', sql.String)
    # TODO: add grid and size

    def toString(self):
        entry = "id=" + str(self.id) + " datetime=" + str(self.dateTime) + \
              " endpoint=" + str(self.endPoint) + " message=" + str(self.message) + "; "
        return entry


# Class used to log data to DB
class Logger():

    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def write(self, message, endpoint):
        Session = sessionmaker(bind=engine)
        session = Session()
        log = Log()
        log.dateTime = datetime.datetime.now()
        log.endPoint = str(endpoint)
        log.message = str(message)
        session.add(log)
        session.commit()
        session.close()

    def read_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        logQuery = session.query(Log).all()
        logs = ""
        for l in logQuery:
            logs += l.toString()
        session.close()
        return logs

