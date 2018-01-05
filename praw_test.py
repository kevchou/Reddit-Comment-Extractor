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

def get_submissions(subreddit, start, end):
    """Get the submission ids for all posts in input $subreddit between
    input dates, $start and $end
    """
    dates = date_range(start, end)

    all_submissions = {}
    sr = reddit.subreddit(subreddit)

    # Gets submission ids of all posts for each day
    for i in range(len(dates) - 1):
        day_submissions = sr.submissions(start=dates[i].timestamp(),
                                         end=dates[i+1].timestamp()-1)

        submission_ids = [sub.id for sub in day_submissions]
        all_submissions[dates[i].strftime("%Y-%m-%d")] = submission_ids 
        print(f"{dates[i]}: {len(submission_ids)} submissions")

    return all_submissions


reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='commentextractor by kevchou')

get_submissions('cryptocurrency', start='2017-01-01', end='2017-01-10')




dates = date_range('2017-01-01', '2017-02-01')

all_submissions = {}
sr = reddit.subreddit('cryptocurrency')

# Gets submission ids of all posts for each day
for i in range(len(dates) - 1):
    print(dates[i])
    day_submissions = sr.submissions(start=dates[i].timestamp(),
                                        end=dates[i+1].timestamp()-1)

    submission_ids = [sub.id for sub in day_submissions]
    all_submissions[dates[i].strftime("%Y-%m-%d")] = submission_ids 
    print(f"{dates[i]}: {len(submission_ids)} submissions")
