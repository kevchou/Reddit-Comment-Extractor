import praw
import pandas as pd
from secret import CLIENT_ID, CLIENT_SECRET

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='commentextractor by kevchou')

subreddit = reddit.subreddit('cryptocurrency')

dates = pd.date_range(start='2017-01-01', end='2018-01-01', freq='D').tolist()

all_submissions = {}

for i in range(len(dates) - 1):
    # Gets submission ids of all posts for each day
    day_submissions = subreddit.submissions(start=dates[i].timestamp(),
                                            end=dates[i+1].timestamp()-1)

    sub_ids = [sub.id for sub in day_submissions]

    all_submissions[dates[i].strftime("%Y-%m-%d")] = sub_ids

    print(f"{dates[i]}: {len(sub_ids)} submissions")
