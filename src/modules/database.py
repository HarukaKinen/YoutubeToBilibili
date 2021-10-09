import enum
from sqlalchemy import Column, String, Integer, create_engine, insert
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from .config import config

config.read()
base = declarative_base()

def create_session(user, password, host, database_name):
    try:
        engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database_name}")
        se = sessionmaker(bind=engine, autocommit=True, autoflush=True)
        # https://farer.org/2017/10/28/sqlalchemy_scoped_session
        session = scoped_session(se)
        return session
    except:
        pass

@enum.unique
class status(enum.IntEnum):
    new, downloaded, uploaded, error = range(1, 5)

class channel(base):
    __tablename__ = "channel"

    channel_id = Column(String(255), primary_key=True)
    subscribe_mode = Column(String(255))
    type = Column(Integer)

    @classmethod
    def add_channel(cls, **kwargs):
        channel = cls(**kwargs)
        se.add(channel)

class task(base):
    __tablename__ = "task"
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

class channel_type(base):
    __tablename__ = "channel_type"
    row_ = Column(Integer, primary_key=True, autoincrement=True, default=1)
    tag = Column(String(255))
    category_id = Column(Integer, default=0)
    description_length = Column(Integer, default=2000)


se = create_session(config.database_user, config.database_password, config.database_host, config.database_name)