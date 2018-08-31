#### SQLAlchemy model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Integer, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

import praw
from datetime import datetime, timedelta
from secret import CLIENT_ID, CLIENT_SECRET


def get_top_submissions(subreddit, reddit, time_filter='all', ):
    """Get top submissions
    """
    sr = reddit.subreddit(subreddit)

    day_submissions = sr.top(time_filter=time_filter)

    submissions = [Submission(id=sub.id,
                                created_date=datetime.fromtimestamp(sub.created_utc),
                                title=sub.title,
                                body=sub.selftext,
                                author=sub.author.name if sub.author else None,
                                score=sub.score,
                                stickied=sub.stickied)
                    for sub in day_submissions]

    return submissions

def get_comments_for_submission(submission_id, reddit):
    """Input a submission id and returns an array of Comment objects
    """
    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=None)

    comments = []

    for c in submission.comments.list():
        if c.body != '[deleted]':
            comments.append(Comment(id=c.id,
                                    submission_id=submission_id,
                                    author=c.author.name if c.author else None,
                                    created_date=datetime.fromtimestamp(c.created_utc),
                                    text=c.body,
                                    score=c.score))
    return comments


# Create SQLAlchemy instances
engine = create_engine('sqlite:///redditcomments.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create Reddit instances
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='commentextractor by kevchou')

# Get all submissions
all_submissions = get_top_submissions('news', reddit=reddit)

# Add all submissions to DB
session.add_all(all_submissions)
session.commit()

# Get all comments from every submission and add to DB
for submission in session.query(Submission).all():
    print(submission.id)
    comments = get_comments_for_submission(submission.id, reddit)
    session.add_all(comments)
    session.commit()



