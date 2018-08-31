#### SQLAlchemy model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Integer, Boolean

Base = declarative_base()

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(String, primary_key=True)
    title = Column(String)
    body = Column(String)
    score = Column(Integer)
    author = Column(String)
    created_date = Column(Date)
    stickied = Column(Boolean)

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(String, primary_key=True)
    submission_id = Column(String)
    author = Column(String)
    created_date = Column(Date)
    text = Column(String)
    score = Column(Integer)
