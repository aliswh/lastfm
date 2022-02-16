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

def get_new_friends(user, MAX=20):
    """ Returns friends and friends of friends of seed user until len(user_pool) gets to MAX.
    """
    def get_friend(theuser):
        for friend in theuser.get_friends(limit=100):
            if len(get_friend.user_pool) < MAX and friend not in get_friend.user_pool:
              get_friend.user_pool.append(friend)
        if len(get_friend.user_pool) < MAX:
            get_friend.index += 1
            get_friend(get_friend.user_pool[index])
    get_friend.user_pool = []
    get_friend.index = 0
    get_friend(user)
    return get_friend.user_pool 


### EXAMPLES, DELETE
p = PyLastSource(AUTH_DATA)

onemonthago = timestamp_x_days_ago(30)
print(datetime.fromtimestamp(onemonthago))

SEED_USER = 'dars4' # random user name found on last.fm
someuser = p.get('user', False, SEED_USER)
user_pool = get_new_friends(someuser, MAX=3)

for user in user_pool:
    p.get('recent_tracks', True, user, limit=10,  time_to=onemonthago)