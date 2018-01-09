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

def date_range(start, end):
    """Get list of dates between $start and $end.
    Inputs: datetime objects or strings formatted as "%Y-%m-%d"
    """

    dates = []

    try:
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
    except:
        pass
    finally:
        delta = end - start

        for i in range(delta.days + 1):
            dates.append(start + timedelta(days=i))

    return dates


def get_submissions(subreddit, start, end, reddit):
    """Get the submission ids for all posts in input $subreddit between
    input dates, $start and $end
    """
    dates = date_range(start, end)

    all_submissions = []
    sr = reddit.subreddit(subreddit)

    # Gets submission ids of all posts for each day
    for i in range(len(dates) - 1):
        day_submissions = sr.submissions(start=dates[i].timestamp(), end=dates[i+1].timestamp()-1)

        submissions = [Submission(id=sub.id,
                                  created_date=datetime.fromtimestamp(sub.created_utc),
                                  title=sub.title,
                                  body=sub.selftext,
                                  author=sub.author.name,
                                  score=sub.score,
                                  stickied=sub.stickied)
                       for sub in day_submissions]

        all_submissions = all_submissions + submissions

    return all_submissions

def get_comments_from_posts(submission_id, reddit):
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
all_submissions = get_submissions('cryptocurrency', '2017-01-01', '2017-12-31', reddit)

# Add all submissions to DB
session.add_all(all_submissions)
session.commit()

# Get all comments from every submission and add to DB
for submission in session.query(Submission).all():
    print(submission.id)
    comments = get_comments_from_posts(submission.id, reddit)
    session.add_all(comments)
    session.commit()



