import enum
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import config

config.read()

base = declarative_base()

def create_session(user, password, host, database_name):
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(user, password, host, database_name))
    se = sessionmaker(bind=engine, autocommit=True)
    # https://farer.org/2017/10/28/sqlalchemy_scoped_session
    session = scoped_session(se)
    return session

@enum.unique
class status(enum.IntEnum):
    new, downloaded, uploaded, error = range(1, 5)

class channel(base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))

class task(base):
    __tablename__ = "tasks"
    id = Column(String(255), primary_key=True)
    status = Column(Integer, default=status.new.value)

    @classmethod
    def add_task(cls, **kwargs):
        task = cls(**kwargs)
        se.add(task)

    @classmethod
    def get_task_status(cls, status):
        return se.query(cls).filter(cls.status == status).all()

    def get_video_id(self):
        return self.id

    def get_video_status(self):
        return self.status

se = create_session(config.database_user, config.database_password, config.database_host, config.database_name)
