from config import AUTH_DATA
from pylastsource import PyLastSource
import time
from datetime import datetime, date, timedelta

def timestamp_x_days_ago(n_days):
    """ Returns (int) timestamp from X days ago from now.
    """
    d = date.today() - timedelta(days=n_days)
    dt = datetime(
            year=d.year,
            month=d.month,
            day=d.day
        )
    return int(dt.timestamp())




### EXAMPLES, DELETE
p = PyLastSource(AUTH_DATA)

onemonthago = timestamp_x_days_ago(1)
print(datetime.fromtimestamp(onemonthago))

SEED_USER = 'dars4' # random user name found on last.fm
user = p.network.get_user(SEED_USER)
user_json = p.get('user', SEED_USER)
print(user_json)
user_tracks_json = p.get('recent_tracks', SEED_USER, limit=100,  time_to=onemonthago)
print(user_tracks_json)