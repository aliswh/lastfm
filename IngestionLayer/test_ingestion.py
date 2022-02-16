from config import AUTH_DATA
from pylastsource import PyLastSource
import time
from datetime import datetime, date, timedelta

def timestamp_x_days_ago(n_days):
  d = date.today() - timedelta(days=n_days)
  dt = datetime(
        year=d.year,
        month=d.month,
        day=d.day
     )
  return int(dt.timestamp())


### EXAMPLES, DELETE

SEED_USER = 'dars4' # random user found on last.fm
p = PyLastSource(AUTH_DATA)
someuser = p.get('user', False, SEED_USER)
sometrack = p.get('track', False, 'Kim Petras', 'Clarity')
onemonthago = timestamp_x_days_ago(30)
print(datetime.fromtimestamp(onemonthago))
p.get('recent_tracks', True, someuser, limit=100,  time_to=onemonthago)